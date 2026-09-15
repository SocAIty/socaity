"""ChatSocaity request defaults: reasoning_effort stays on the instance."""

from langchain_core.messages import HumanMessage

from socaity.integrations.langchain import ChatSocaity


def test_request_forwards_reasoning_effort():
    model = ChatSocaity(model="https://example.invalid/chat", reasoning_effort="low")
    request = model._request([HumanMessage(content="hi")], None)
    assert request["reasoning_effort"] == "low"
    assert request["messages"][0]["content"] == "hi"


def test_coerce_keeps_remote_image_url():
    from socaity.integrations.langchain.chat import _coerce_message_content

    url = "https://cdn.example.test/monkey.png"
    out = _coerce_message_content([{
        "role": "user",
        "content": [
            {"type": "text", "text": "describe"},
            {"type": "image_url", "image_url": {"url": url}},
        ],
    }])
    assert out[0]["content"][1]["image_url"]["url"] == url
