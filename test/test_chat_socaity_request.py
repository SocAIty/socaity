"""ChatSocaity request defaults: reasoning_effort stays on the instance."""

from langchain_core.messages import HumanMessage

from socaity.integrations.langchain import ChatSocaity


def test_request_forwards_reasoning_effort():
    model = ChatSocaity(model="https://example.invalid/chat", reasoning_effort="low")
    request = model._request([HumanMessage(content="hi")], None)
    assert request["reasoning_effort"] == "low"
    assert request["messages"][0]["content"] == "hi"
