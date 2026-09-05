"""LangChain integration: use Socaity chat services as LangChain chat models.

Requires ``langchain-core>=1.0`` (optional dependency)::

    pip install langchain-core

    from socaity.integrations.langchain import ChatSocaity
    model = ChatSocaity(model="qwen3-5")
    model.invoke("Hello!")
"""

try:
    from socaity.integrations.langchain.chat import ChatSocaity
    from socaity.integrations.langchain.tools import to_langchain
except ImportError as error:
    raise ImportError(
        "The LangChain integration needs langchain-core>=1.0. "
        "Install it with: pip install langchain-core"
    ) from error

__all__ = ["ChatSocaity", "to_langchain"]
