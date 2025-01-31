import os

from socaity.api.text.chat.llama3.meta_llama_3 import MetaLLama3_70b

llama3 = MetaLLama3_70b(service="replicate", api_key=os.getenv("REPLICATE_API_KEY", None))
# fluxs = FluxSchnell(service="socaity_local", api_key=os.getenv("SOCAITY_API_KEY", None))

def test_llama_chat():
    prompt = "Write a poem with 3 sentences why an SDK is so much better than plain web requests."
    fj = llama3.chat(
        prompt=prompt
    )
    generated_text = fj.get_result()
    print(generated_text)


if __name__ == "__main__":
    test_llama_chat()