# backend/services/deepeval_client.py
from deepeval.models.base_model import DeepEvalBaseLLM
from backend.services.databricks_client import chat_complete

_model_instance: "DatabricksLLM | None" = None


class DatabricksLLM(DeepEvalBaseLLM):
    def get_model_name(self) -> str:
        return "databricks"

    def load_model(self):
        return self

    def generate(self, prompt: str) -> str:
        return chat_complete([{"role": "user", "content": prompt}], temperature=0.0)

    async def a_generate(self, prompt: str) -> str:
        return self.generate(prompt)


def get_deepeval_model() -> DatabricksLLM:
    global _model_instance
    if _model_instance is None:
        _model_instance = DatabricksLLM()
    return _model_instance
