# tests/test_deepeval_client.py
from unittest.mock import patch
from backend.services.deepeval_client import DatabricksLLM


def test_adapter_generate_delegates_to_chat_complete():
    with patch("backend.services.deepeval_client.chat_complete", return_value="hello") as mock:
        llm = DatabricksLLM()
        result = llm.generate("test prompt")
    mock.assert_called_once_with([{"role": "user", "content": "test prompt"}], temperature=0.0)
    assert result == "hello"


def test_adapter_get_model_name():
    llm = DatabricksLLM()
    assert llm.get_model_name() == "databricks"


def test_get_deepeval_model_returns_singleton():
    from backend.services.deepeval_client import get_deepeval_model
    m1 = get_deepeval_model()
    m2 = get_deepeval_model()
    assert m1 is m2
