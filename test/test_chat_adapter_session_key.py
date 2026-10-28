"""ChatServiceAdapter reconnects when the entered session key changes."""

from types import SimpleNamespace

from socaity import Session
from socaity.integrations.chat_adapter import ChatServiceAdapter


def _adapter(api_key: str, service: object) -> ChatServiceAdapter:
    adapter = ChatServiceAdapter.__new__(ChatServiceAdapter)
    adapter.client = SimpleNamespace(api_key=api_key, service=service, temporary=True)
    adapter.jobs = []
    adapter.endpoint = SimpleNamespace(path="/chat", parameters=[])
    return adapter


def _session(api_key: str) -> Session:
    return Session(
        api_key=api_key,
        backend_url="http://127.0.0.1:9",
        gate_url="http://127.0.0.1:9",
    )


def test_unchanged_session_key_reuses_the_client(monkeypatch):
    service = object()
    connected = []

    def connect(source, api_key=None, **kwargs):
        connected.append(api_key)
        return SimpleNamespace(api_key=api_key, service=source, temporary=True)

    monkeypatch.setattr("socaity.integrations.chat_adapter.client.connect", connect)
    adapter = _adapter("tk_turn_a", service)

    with _session("tk_turn_a"):
        adapter._bind_session_key()
        adapter._bind_session_key()

    assert connected == []
    assert adapter.client.api_key == "tk_turn_a"


def test_changed_session_key_reconnects_once(monkeypatch):
    service = object()
    connected = []

    def connect(source, api_key=None, **kwargs):
        connected.append((source, api_key))
        return SimpleNamespace(api_key=api_key, service=source, temporary=True)

    monkeypatch.setattr("socaity.integrations.chat_adapter.client.connect", connect)
    adapter = _adapter("tk_turn_a", service)
    previous = adapter.client

    with _session("tk_turn_b"):
        adapter._bind_session_key()
        adapter._bind_session_key()

    assert connected == [(service, "tk_turn_b")]
    assert adapter.client.api_key == "tk_turn_b"
    assert adapter.client.service is service
    assert previous.temporary is False


def test_submit_uses_the_new_session_key(monkeypatch):
    service = object()
    submitted = []

    def connect(source, api_key=None, **kwargs):
        client = SimpleNamespace(api_key=api_key, service=source, temporary=True)

        def submit_job(path, **kwargs):
            submitted.append((client.api_key, path))
            return SimpleNamespace(name="job")

        client.submit_job = submit_job
        return client

    monkeypatch.setattr("socaity.integrations.chat_adapter.client.connect", connect)
    adapter = _adapter("tk_turn_a", service)

    def submit_job(path, **kwargs):
        submitted.append((adapter.client.api_key, path))
        return SimpleNamespace(name="job")

    adapter.client.submit_job = submit_job

    with _session("tk_turn_b"):
        adapter.submit({"messages": [{"role": "user", "content": "hi"}]})
        adapter.submit({"messages": [{"role": "user", "content": "again"}]})

    assert [key for key, _path in submitted] == ["tk_turn_b", "tk_turn_b"]
