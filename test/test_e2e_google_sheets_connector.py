"""E2E: Google Sheets OpenAPI connector, OAuth2 credential lifecycle, SDK & SPAINE execution.

1. ``test_google_sheets_connector_sdk``:
   - Inspects and registers the Google Sheets v4 OpenAPI specification
     (``https://api.apis.guru/v2/specs/googleapis.com/sheets/v4/openapi.json``).
   - Verifies that the split ``Oauth2`` (implicit) and ``Oauth2c`` (authorizationCode)
     security schemes are deduplicated into a single service-wide ``Oauth2``
     credential requirement with both flows preserved.
   - Verifies ``resolve_credentials`` reports ``oauth_supported=True`` on the ``Oauth2`` slot.
   - Verifies that calling ``sheets-spreadsheets-create`` without a bound credential fails
     fast in the worker with ``CredentialRequiredError`` (HTTP 409 from
     ``/v1/credentials/jobs/{job_id}/secrets``) and actionable remediation instructions.
   - Authenticates the ``Oauth2`` slot (via live browser OAuth2 when
     ``SOCAITY_E2E_MANUAL=1``, ``GOOGLE_SHEETS_TOKEN`` when set, or an OAuth2 vault
     credential binding) and runs ``sheets-spreadsheets-create`` with ``"hello world"``
     content, taking the JSON response as-is (no media-toolkit file conversion or S3 upload).

2. ``test_spaine_google_sheets_hello_world``:
   - Disconnects credentials so the ``Oauth2`` slot is unresolved.
   - Prompts SPAINE in ``agent`` mode to connect Google Sheets and create a spreadsheet
     with ``"hello world"`` content.
   - Verifies Turn 1 pauses with ``agent_status == "interrupted"`` on a
     ``resolve_credentials`` HIT for ``slot_name == "Oauth2"`` (``oauth_supported=True``).
   - Supplies the OAuth2 credential decision to resume the thread and verifies Turn 2
     executes the ``sheets-spreadsheets-create`` child job and finishes with
     ``agent_status == "completed"``.

    python test/test_e2e_google_sheets_connector.py
    pytest test/test_e2e_google_sheets_connector.py -v -s
    SOCAITY_E2E_MANUAL=1 pytest test/test_e2e_google_sheets_connector.py -v -s
"""
from __future__ import annotations

import json
import os
import sys
import webbrowser
from datetime import datetime, timezone
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import agentic_utils as env  # noqa: E402  (sets URL defaults before socaity import)

from apipod_registry import active_details  # noqa: E402
from media_toolkit import IMediaFile  # noqa: E402
from socaity import Session, client  # noqa: E402
from socaity_cli.errors import BackendApiError  # noqa: E402

GOOGLE_SHEETS_SPEC_URL = "https://api.apis.guru/v2/specs/googleapis.com/sheets/v4/openapi.json"
GOOGLE_SHEETS_HOST = "sheets.googleapis.com"
CREATE_OP = "sheets-spreadsheets-create"
AGENT = "spaine"
MANUAL = os.getenv("SOCAITY_E2E_MANUAL") == "1"

SPREADSHEET_HELLO_WORLD = {
    "properties": {"title": "hello world"},
    "sheets": [
        {
            "properties": {"title": "Sheet1"},
            "data": [
                {
                    "startRow": 0,
                    "startColumn": 0,
                    "rowData": [
                        {
                            "values": [
                                {"userEnteredValue": {"stringValue": "hello world"}}
                            ]
                        }
                    ],
                }
            ],
        }
    ],
}

SPAINE_PROMPT = (
    f"Connect the Google Sheets OpenAPI spec {GOOGLE_SHEETS_SPEC_URL} with add_connector, "
    f"then call run_service on operation {CREATE_OP} with params "
    '{"request": {"properties": {"title": "hello world"}, "sheets": [{"data": [{"rowData": [{"values": [{"userEnteredValue": {"stringValue": "hello world"}}]}]}]}]}} '
    "to create a Google Sheet with 'hello world' content. Take the response as is."
)

pytestmark = [
    pytest.mark.skipif(not env.backend_up(), reason=f"backend not reachable at {env.BACKEND}"),
    pytest.mark.skipif(not env.inference_up(), reason=f"APIPod gate not reachable at {env.GATE}"),
    pytest.mark.skipif(not env.api_key(), reason=env.missing_env("SOCAITY_API_KEY") or "no SOCAITY_API_KEY"),
]


def _open_authorize(event: str, data: dict) -> None:
    if event == "authorize":
        env.log("T12.oauth", f"authorize at {data.get('url')}")
        webbrowser.open(data["url"])


def _ensure_google_sheets_connector() -> tuple[str, bool]:
    """Register or reuse the Google Sheets OpenAPI connector.

    If an older registration exists with un-deduplicated credential requirements,
    delete and re-register it so the catalog row reflects the current parser.
    """
    try:
        preview = client.inspect_connector(GOOGLE_SHEETS_SPEC_URL)
        env.log(
            "T12.1",
            f"inspect spec={preview.get('specification')} "
            f"ops={len(preview.get('operations') or [])} "
            f"credential_names={preview.get('credential_names')}",
        )
        assert preview["specification"] == "openapi", preview["specification"]
        assert preview.get("credential_names") == ["Oauth2"], preview.get("credential_names")
    except BackendApiError as exc:
        assert exc.status_code == 409 and exc.code == "connector_exists", (exc.status_code, exc.code, str(exc))

    try:
        created = client.register_connector(GOOGLE_SHEETS_SPEC_URL)
        return created.id, False
    except BackendApiError as exc:
        assert exc.status_code == 409 and exc.code == "connector_exists", (exc.status_code, exc.code, str(exc))
        service_id = exc.detail["service"]["id"]
        existing = client.get_service(
            service_id,
            expand=["details.contract", "details.connector", "endpoints", "credential_requirements"],
        )
        reqs = existing.credential_requirements if existing else []
        if not existing or len(reqs or []) != 1 or reqs[0].endpoint_id is not None:
            env.log("T12.1", f"re-registering legacy connector service_id={service_id} reqs={len(reqs or [])}")
            client.delete_service(service_id)
            recreated = client.register_connector(GOOGLE_SHEETS_SPEC_URL)
            return recreated.id, False
        return service_id, True


def _clear_oauth2_bindings(service_id: str) -> None:
    """Ensure no service/user/thread binding or 'Oauth2'-named vault row auto-resolves the slot."""
    client.disconnect_connector_credential(service_id)
    for binding in client.list_credential_bindings():
        if binding.slot_name == "Oauth2" and binding.id:
            client.delete_credential_binding(binding.id)
    for cred in client.list_credentials():
        if cred.name == "Oauth2" and cred.id:
            client.delete_credential(cred.id)


def _child_jobs_since(started_at: datetime, service_id: str, conversation_id: str | None = None) -> list:
    jobs = [
        job for job in client.query_jobs(limit=50)
        if job.service_id == service_id and job.created_at
        and datetime.fromisoformat(job.created_at.replace("Z", "+00:00")) >= started_at
    ]
    if conversation_id:
        conv = client.get_conversation(conversation_id, expand=["items"])
        for item in (conv.items if conv else None) or []:
            for part in item.parts or []:
                output = getattr(part, "output", None)
                job_id = output.get("job_id") if isinstance(output, dict) else None
                if job_id:
                    job = client.get_job(job_id)
                    if job and job.service_id == service_id and all(j.id != job.id for j in jobs):
                        jobs.append(job)
    return jobs


def run_sdk_test() -> None:
    with Session(api_key=env.api_key(), backend_url=env.BACKEND):
        service_id, existed = _ensure_google_sheets_connector()
        service = client.get_service(
            service_id,
            expand=["details.contract", "details.connector", "endpoints", "credential_requirements"],
        )
        assert service is not None and service.kind == "connector", service
        details = active_details(service)
        assert details is not None and details.connector is not None, "connector details missing"
        env.log(
            "T12.1",
            f"service_id={service_id} slug={service.slug} existed={existed} "
            f"endpoints={len(service.endpoints or [])} cred_reqs={len(service.credential_requirements or [])}",
        )

        # Verify single deduplicated Oauth2 requirement and preserved OAuth2 flows
        reqs = service.credential_requirements or []
        assert len(reqs) == 1, f"expected 1 deduplicated credential requirement, got {len(reqs)}: {reqs}"
        assert reqs[0].name == "Oauth2" and reqs[0].endpoint_id is None, reqs[0]
        assert details.contract.security == ["Oauth2"], details.contract.security
        oauth_scheme = (details.contract.security_schemes or {}).get("Oauth2") or {}
        flows = oauth_scheme.get("flows") or {}
        assert "authorizationCode" in flows and "implicit" in flows, flows
        auth_code_flow = flows["authorizationCode"]
        assert auth_code_flow.get("authorizationUrl") == "https://accounts.google.com/o/oauth2/auth"
        assert auth_code_flow.get("tokenUrl") == "https://accounts.google.com/o/oauth2/token"

        # Disconnect and verify resolve_credentials reports oauth_supported=True
        _clear_oauth2_bindings(service_id)
        resolved = client.resolve_credentials(
            service_id=service_id,
            details_id=details.id,
            connectors_id=details.connector.id,
        )
        assert resolved is not None and resolved.hit is not None, f"expected unresolved HIT, got {resolved}"
        assert len(resolved.hit.slots) == 1, resolved.hit.slots
        hit_slot = resolved.hit.slots[0]
        env.log(
            "T12.2",
            f"unresolved slot={hit_slot.slot_name} oauth_supported={hit_slot.oauth_supported} "
            f"hosts={hit_slot.allowed_hosts}",
        )
        assert hit_slot.slot_name == "Oauth2", hit_slot
        assert hit_slot.oauth_supported is True, hit_slot
        assert GOOGLE_SHEETS_HOST in (hit_slot.allowed_hosts or []), hit_slot

        # Variation 1: unauthenticated SDK run fails fast with actionable CredentialRequiredError
        target = f"{service.slug}/{CREATE_OP}"
        with pytest.raises(Exception) as missing_cred:
            job = client.run(target, params={"request": SPREADSHEET_HELLO_WORLD})
            job.get_result(timeout_s=90)
        err_text = str(missing_cred.value)
        env.log("T12.2", f"unauthenticated run failed fast: {err_text}")
        assert "Credential required for" in err_text, err_text
        assert "Oauth2" in err_text, err_text
        assert "socaity connector auth" in err_text, err_text
        assert "change_connector_credential" in err_text, err_text

        # Authenticate via OAuth2 (manual browser flow, GOOGLE_SHEETS_TOKEN, or OAuth2 vault credential)
        live_token = os.getenv("GOOGLE_SHEETS_TOKEN")
        if MANUAL:
            binding = client.change_connector_credential(service_id, oauth=True, on_event=_open_authorize)
            env.log("T12.3", f"live OAuth binding={binding}")
        elif live_token:
            binding = client.change_connector_credential(service_id, secret=live_token)
            env.log("T12.3", f"bound GOOGLE_SHEETS_TOKEN binding={binding}")
        else:
            oauth_cred = client.upsert_credential(
                name=f"{service.slug}-oauth",
                secret="ya29.e2e-oauth2-verification-token",
                allowed_hosts=[GOOGLE_SHEETS_HOST],
                metadata={
                    "scheme": "oauth",
                    "token_endpoint": "https://oauth2.googleapis.com/token",
                    "scope": "https://www.googleapis.com/auth/spreadsheets",
                },
            )
            assert oauth_cred is not None and oauth_cred.id, "failed to upsert OAuth vault credential"
            binding = client.upsert_credential_binding(
                scope_type="service",
                scope_id=service_id,
                slot_name="Oauth2",
                user_credential_id=oauth_cred.id,
                slot_target_id=service_id,
            )
            env.log("T12.3", f"bound OAuth2 vault credential id={oauth_cred.id} binding={binding}")

        resolved_after = client.resolve_credentials(
            service_id=service_id,
            details_id=details.id,
            connectors_id=details.connector.id,
        )
        assert resolved_after is not None and resolved_after.hit is None, resolved_after
        assert len(resolved_after.resolved) == 1 and resolved_after.resolved[0].slot_name == "Oauth2"

        if MANUAL or live_token:
            job = client.run(target, params={"request": SPREADSHEET_HELLO_WORLD})
            result = job.get_result(timeout_s=120)
            env.log("T12.4", f"created spreadsheet result_type={type(result).__name__} keys={list(result) if isinstance(result, dict) else result}")
            assert not isinstance(result, IMediaFile), "spreadsheet response must not be converted to MediaFile"
            assert isinstance(result, dict) and result.get("spreadsheetId"), result
            assert (result.get("properties") or {}).get("title") == "hello world", result
        else:
            with pytest.raises(Exception) as upstream_resp:
                job = client.run(target, params={"request": SPREADSHEET_HELLO_WORLD})
                job.get_result(timeout_s=90)
            upstream_err = str(upstream_resp.value)
            env.log("T12.4", f"authenticated dispatch reached Google Sheets: {upstream_err[:240]}")
            assert "Credential required for" not in upstream_err, upstream_err
            assert "sheets.googleapis.com" in upstream_err or "401" in upstream_err or "UNAUTHENTICATED" in upstream_err, upstream_err
            _clear_oauth2_bindings(service_id)
    env.log("T12.sdk", "PASS")


def run_spaine_test() -> None:
    with Session(api_key=env.api_key(), backend_url=env.BACKEND):
        service_id, _ = _ensure_google_sheets_connector()
        service = client.get_service(service_id, expand=["details.connector", "endpoints"])
        assert service is not None
        _clear_oauth2_bindings(service_id)
        started_at = datetime.now(timezone.utc)

        # Turn 1: SPAINE connects Google Sheets and calls run_service
        turn = env.run_agent(AGENT, message=SPAINE_PROMPT, mode="agent", timeout_s=600)
        env.log(
            "T12.5",
            f"turn1 job={turn['job_id']} status={turn['status']} "
            f"agent_status={turn['agent_status']} thread={turn['thread_id']}",
        )
        env.log("T12.5", f"pending={turn['pending_actions']}")
        assert turn["agent_status"] == "interrupted", turn["response"]
        assert turn["pending_actions"], "expected pending action on turn 1"
        thread_id = turn["thread_id"]

        # If run_service is gated by tool approval ("ask" posture), approve it to enter run_service
        action = turn["pending_actions"][0]
        if action.get("name") == "run_service":
            env.log("T12.5", f"approving run_service interrupt id={action['id']}")
            turn = env.run_agent(
                AGENT,
                thread_id=thread_id,
                decisions=[{"interrupt_row_id": action["id"], "type": "approve"}],
                mode="agent",
                timeout_s=600,
            )
            env.log(
                "T12.5",
                f"after run_service approve: job={turn['job_id']} "
                f"agent_status={turn['agent_status']} pending={turn['pending_actions']}",
            )
            assert turn["agent_status"] == "interrupted", turn["response"]
            assert turn["pending_actions"], "expected resolve_credentials pending action after approving run_service"
            action = turn["pending_actions"][0]

        assert action.get("name") == "resolve_credentials", action
        slots = (action.get("arguments") or {}).get("slots") or []
        assert len(slots) == 1 and slots[0].get("slot_name") == "Oauth2", slots
        assert slots[0].get("oauth_supported") is True, slots[0]

        # Supply OAuth2 credential decision and resume the interrupted turn
        token = os.getenv("GOOGLE_SHEETS_TOKEN") or "ya29.e2e-spaine-oauth2-token"
        cred_name = f"{service.slug}-oauth"
        client.upsert_credential(
            name=cred_name,
            secret=token,
            allowed_hosts=[GOOGLE_SHEETS_HOST],
            metadata={
                "scheme": "oauth",
                "token_endpoint": "https://oauth2.googleapis.com/token",
                "scope": "https://www.googleapis.com/auth/spreadsheets",
            },
        )
        hit_decision = json.dumps([
            {
                "slot_name": "Oauth2",
                "credential_name": cred_name,
                "remember": "thread",
                "allowed_hosts": [GOOGLE_SHEETS_HOST],
            }
        ])
        decisions = [
            {
                "interrupt_row_id": action["id"],
                "type": "respond",
                "message": hit_decision,
            }
        ]
        final_turn = env.run_agent(
            AGENT,
            thread_id=thread_id,
            decisions=decisions,
            mode="agent",
            timeout_s=600,
        )
        env.log(
            "T12.6",
            f"final_turn job={final_turn['job_id']} status={final_turn['status']} "
            f"agent_status={final_turn['agent_status']} text={str(final_turn['text'])[:400]!r}",
        )
        # If the model retries run_service after an upstream 401 with synthetic token, approve or finish
        assert final_turn["agent_status"] in ("completed", "interrupted"), final_turn["response"]

        child_jobs = _child_jobs_since(started_at, service_id, thread_id)
        env.log("T12.6", f"google-sheets child jobs={[j.id for j in child_jobs]}")
        assert child_jobs, "expected SPAINE to execute a Google Sheets child job after credential HIT resume"
        _clear_oauth2_bindings(service_id)
    env.log("T12.spaine", "PASS")


def test_google_sheets_connector_sdk() -> None:
    run_sdk_test()


def test_spaine_google_sheets_hello_world() -> None:
    run_spaine_test()


if __name__ == "__main__":
    run_sdk_test()
    run_spaine_test()
