import os

from socaity import DeepSeekR1

chat_model = DeepSeekR1()
#chat_model = DeepSeekR1(service="replicate", api_key=os.getenv("REPLICATE_API_KEY", None))
# fluxs = FluxSchnell(service="socaity_local", api_key=os.getenv("SOCAITY_API_KEY", None))

def test_chat():
    prompt = "Write a poem with 3 sentences why an SDK is so much better than plain web requests."
    fj = chat_model.chat(
        prompt=prompt
    )
    generated_text = fj.get_result()
    print(generated_text)


if __name__ == "__main__":
    test_chat()