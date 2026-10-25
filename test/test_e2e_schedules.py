"""E2E Test 1: Schedule-Core (`docs/planned/schedules.md`).

Tests one service schedule on official `qwen3.8` chat (`FREQ=SECONDLY;INTERVAL=5`):
1. Cold start / overlap rule: while the first job stays active, due instants are
   recorded as `skipped` and the schedule stays `enabled`.
2. Upsert `INTERVAL=10` (`dtstart` stays put): reads `next_run_at` as `T`,
   verifies no occurrence fires on the old 5s grid and the next `fired` row is `T`.
   Adds two `EXDATE`s for the two instants after the next one, verifies they are
   `excluded`, and verifies the instant after them (`+30s` gap) fires after a run
   finishes inside the 10s interval.
3. Deletes the schedule: `get_schedule` returns `None` and the next interval
   creates no new job.
"""

from __future__ import annotations

import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import agentic_utils as env  # noqa: E402

from socaity import Session, client  # noqa: E402


def format_utc_instant(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).replace(microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_utc_instant(raw: str) -> datetime:
    dt = datetime.fromisoformat(raw.strip().replace("Z", "+00:00"))
    return (dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)).astimezone(timezone.utc).replace(microsecond=0)

pytestmark = [
    pytest.mark.skipif(not env.backend_up(), reason=f"backend not reachable at {env.BACKEND}"),
    pytest.mark.skipif(not env.inference_up(), reason=f"APIPod gate not reachable at {env.GATE}"),
    pytest.mark.skipif(not env.api_key(), reason=env.missing_env("SOCAITY_API_KEY") or "no SOCAITY_API_KEY"),
]

QWEN_SERVICE = "qwen3-8-official"


def _wait_for_first_fired_and_skipped(schedule_id: str, timeout_s: float = 180.0) -> tuple[str, list]:
    """Wait until the schedule has at least one `fired` row and at least one `skipped` row."""
    deadline = time.monotonic() + timeout_s
    while time.monotonic() < deadline:
        occs = client.get_schedule_occurrences(schedule_id)
        fired = [o for o in occs if o.status == "fired" and o.job_id]
        skipped = [o for o in occs if o.status == "skipped"]
        if fired and skipped:
            return str(fired[0].job_id), occs
        time.sleep(0.5)
    occs = client.get_schedule_occurrences(schedule_id)
    raise AssertionError(f"Timed out waiting for fired + skipped occurrences; got: {[o.model_dump() for o in occs]}")


def _wait_job_finished(job_id: str, timeout_s: float = 300.0) -> dict:
    res = env.poll_job(job_id, timeout_s=timeout_s)
    assert res.get("status") == "finished", f"Expected job {job_id} to finish, got: {res}"
    return res


def _wait_for_active_job_to_finish(schedule_id: str, min_lead_s: float = 0.8, timeout_s: float = 180.0) -> None:
    """Wait until the latest fired job finishes and `next_run_at` is still ahead."""
    deadline = time.monotonic() + timeout_s
    while time.monotonic() < deadline:
        occs = client.get_schedule_occurrences(schedule_id)
        fired = [o for o in occs if o.status == "fired" and o.job_id]
        if fired:
            latest_job_id = str(fired[-1].job_id)
            _wait_job_finished(latest_job_id, timeout_s=180.0)
        sched = client.get_schedule(schedule_id)
        assert sched is not None and sched.enabled and sched.next_run_at
        next_dt = parse_utc_instant(sched.next_run_at)
        lead = (next_dt - datetime.now(timezone.utc)).total_seconds()
        if lead >= min_lead_s:
            return
        time.sleep(0.2)
    raise AssertionError("Could not find a quiet window before next_run_at")


def run() -> None:
    session = Session(api_key=env.api_key(), backend_url=env.BACKEND, gate_url=env.GATE)
    with session:
        schedule_id = None
        try:
            dtstart_dt = datetime.now(timezone.utc).replace(microsecond=0) + timedelta(seconds=1)
            dtstart_iso = format_utc_instant(dtstart_dt)
            env.log("T1.1", f"Creating schedule on {QWEN_SERVICE} dtstart={dtstart_iso} FREQ=SECONDLY;INTERVAL=5")

            sched = client.create_schedule(
                target_type="service/endpoint",
                target_id=QWEN_SERVICE,
                tzid="UTC",
                dtstart=dtstart_iso,
                rrule="FREQ=SECONDLY;INTERVAL=5",
                inputs={
                    "messages": [
                        {
                            "role": "user",
                            "content": (
                                "Write a numbered list from 1 to 20 where each line is "
                                "'<n>: The quick brown fox jumps over the lazy dog', "
                                "and at the very end output the word pong."
                            ),
                        }
                    ],
                    "max_tokens": 900,
                },
            )
            assert sched is not None and sched.id, "create_schedule returned None"
            schedule_id = sched.id
            env.log("T1.1", f"Created schedule id={schedule_id} next_run_at={sched.next_run_at}")

            # 1. Cold start / overlap rule: first job stays active >5s, so later instants are skipped.
            first_job_id, occs = _wait_for_first_fired_and_skipped(schedule_id, timeout_s=180.0)
            skipped_count = sum(1 for o in occs if o.status == "skipped")
            sched_now = client.get_schedule(schedule_id)
            assert sched_now is not None and sched_now.enabled is True
            env.log(
                "T1.1",
                f"Overlap verified: first_job_id={first_job_id} skipped={skipped_count} enabled={sched_now.enabled}",
            )

            # Wait for the active job to finish and ensure the next instant is still ahead.
            first_res = _wait_job_finished(first_job_id, timeout_s=300.0)
            env.log("T1.1", f"First job finished: {str(first_res.get('result'))[:120]}")
            _wait_for_active_job_to_finish(schedule_id, min_lead_s=0.8)

            # 2. Upsert INTERVAL=10 while next instant is ahead. dtstart stays put.
            before_update = client.get_schedule(schedule_id)
            assert before_update is not None
            fired_before_T = {
                o.occurrence_at for o in client.get_schedule_occurrences(schedule_id) if o.status == "fired"
            }

            updated = client.update_schedule(
                schedule_id,
                rrule="FREQ=SECONDLY;INTERVAL=10",
                inputs={
                    "messages": [{"role": "user", "content": "Reply with the single word pong only, no explanation."}],
                    "max_tokens": 16,
                },
            )
            assert updated is not None
            assert updated.dtstart == dtstart_iso, f"dtstart changed: {updated.dtstart} != {dtstart_iso}"
            assert updated.next_run_at is not None
            T_iso = updated.next_run_at
            T_dt = parse_utc_instant(T_iso)
            offset_from_dtstart = int((T_dt - dtstart_dt).total_seconds())
            assert offset_from_dtstart % 10 == 0, f"T={T_iso} is not on the 10s grid from dtstart={dtstart_iso}"
            env.log("T1.2", f"Upserted INTERVAL=10; dtstart={updated.dtstart} T={T_iso}")

            # Wait until T fires and verify no occurrence fired on an odd 5-second instant.
            deadline = time.monotonic() + 60.0
            fired_T_occ = None
            while time.monotonic() < deadline:
                occs = client.get_schedule_occurrences(schedule_id)
                new_fired = [o for o in occs if o.status == "fired" and o.occurrence_at not in fired_before_T]
                if new_fired:
                    fired_T_occ = new_fired[0]
                    break
                time.sleep(0.3)

            assert fired_T_occ is not None, f"Expected occurrence at T={T_iso} to fire"
            assert fired_T_occ.occurrence_at == T_iso, (
                f"Expected next fired row to be T={T_iso}, got {fired_T_occ.occurrence_at}"
            )
            env.log("T1.2", f"Verified next fired occurrence is T={T_iso} (job_id={fired_T_occ.job_id})")

            # Wait for T's job to finish, then set up two EXDATEs for the two instants after the next one.
            _wait_job_finished(str(fired_T_occ.job_id), timeout_s=180.0)
            _wait_for_active_job_to_finish(schedule_id, min_lead_s=1.5)

            sched_before_ex = client.get_schedule(schedule_id)
            assert sched_before_ex is not None and sched_before_ex.next_run_at
            next_one_dt = parse_utc_instant(sched_before_ex.next_run_at)
            next_one_iso = format_utc_instant(next_one_dt)
            ex1_dt = next_one_dt + timedelta(seconds=10)
            ex2_dt = next_one_dt + timedelta(seconds=20)
            after_ex_dt = next_one_dt + timedelta(seconds=30)
            ex1_iso = format_utc_instant(ex1_dt)
            ex2_iso = format_utc_instant(ex2_dt)
            after_ex_iso = format_utc_instant(after_ex_dt)

            with_ex = client.update_schedule(schedule_id, exdates=[ex1_iso, ex2_iso])
            assert with_ex is not None
            env.log(
                "T1.2",
                f"Added EXDATEs [{ex1_iso}, {ex2_iso}] after next={next_one_iso}; expecting fire at {after_ex_iso}",
            )

            occs_with_ex = client.get_schedule_occurrences(schedule_id)
            excluded_at = {o.occurrence_at for o in occs_with_ex if o.status == "excluded"}
            assert ex1_iso in excluded_at and ex2_iso in excluded_at, f"Missing excluded rows: {excluded_at}"

            # Wait for next_one_iso to fire and finish inside the 10-second interval, then wait for after_ex_iso.
            deadline = time.monotonic() + 90.0
            fired_after_ex = None
            while time.monotonic() < deadline:
                occs = client.get_schedule_occurrences(schedule_id)
                fired_map = {o.occurrence_at: o for o in occs if o.status == "fired"}
                if after_ex_iso in fired_map:
                    fired_after_ex = fired_map[after_ex_iso]
                    break
                time.sleep(0.4)

            assert fired_after_ex is not None, f"Expected {after_ex_iso} to fire after EXDATE gap"
            occs_after = client.get_schedule_occurrences(schedule_id)
            fired_set = {o.occurrence_at for o in occs_after if o.status == "fired"}
            assert ex1_iso not in fired_set and ex2_iso not in fired_set, (
                f"Excluded instants should not have fired: {fired_set}"
            )
            assert next_one_iso in fired_set and after_ex_iso in fired_set
            gap_s = (parse_utc_instant(after_ex_iso) - parse_utc_instant(next_one_iso)).total_seconds()
            assert gap_s == 30.0, f"Expected 30s gap across two EXDATEs, got {gap_s}s"
            env.log("T1.2", f"Verified EXDATE gap={gap_s}s: {next_one_iso} -> {after_ex_iso}")

            # 3. Delete the schedule. The GET is gone. The next interval creates no new job.
            deleted = client.delete_schedule(schedule_id)
            assert deleted is True, "delete_schedule returned False"
            assert client.get_schedule(schedule_id) is None, "get_schedule should return None after delete"
            jobs_before_wait = {j.id for j in client.query_jobs(limit=25)}
            env.log("T1.3", f"Schedule {schedule_id} deleted; waiting 12s to verify no new job is created")
            schedule_id_deleted = schedule_id
            schedule_id = None
            time.sleep(12.0)
            assert client.get_schedule(schedule_id_deleted) is None
            jobs_after_wait = {j.id for j in client.query_jobs(limit=25)}
            new_jobs = jobs_after_wait - jobs_before_wait
            assert not new_jobs, f"Expected no new jobs after schedule delete, found: {new_jobs}"
            env.log("T1.3", "Verified no new job created after schedule delete")
        finally:
            if schedule_id:
                try:
                    client.delete_schedule(schedule_id)
                except Exception as exc:
                    env.log("cleanup", f"delete_schedule warning: {exc}")

    env.log("done", "PASS")


def test_schedule_core() -> None:
    run()


if __name__ == "__main__":
    run()
