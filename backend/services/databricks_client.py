from openai import OpenAI
from backend.services.config_manager import config_manager


def get_llm_client() -> tuple[OpenAI, str]:
    cfg = config_manager.load()
    llm_url = cfg["llm_endpoint_url"]
    token = cfg["api_token"]

    # Strip /invocations — openai SDK appends /chat/completions itself
    base_url = llm_url.removesuffix("/invocations")
    # Model name is the last path segment
    model_name = base_url.rstrip("/").split("/")[-1]
    # base_url must be the serving-endpoints parent
    serving_base = base_url.rsplit("/", 1)[0] + "/"

    client = OpenAI(api_key=token, base_url=serving_base)
    return client, model_name


def chat_complete(messages: list[dict], temperature: float = 0.2) -> str:
    client, model_name = get_llm_client()
    response = client.chat.completions.create(
        model=model_name,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message.content
