import os
from socaity.sdk.replicate.deepseek_ai import deepseek_v3


def test_deepseek_v3():
    chat_model = deepseek_v3(api_key=os.getenv("SOCAITY_API_KEY"))
    prompt = "Write a poem with 3 sentences why an SDK is so much better than plain web requests."
    fj = chat_model(prompt=prompt)
    generated_text = fj.get_result()
    print(generated_text)


if __name__ == "__main__":
    test_deepseek_v3()
