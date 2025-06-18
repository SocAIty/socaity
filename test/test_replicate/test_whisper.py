import os

from socaity.sdk.replicate.vaibhavs10 import incredibly_fast_whisper

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
INPUT_AUDIO = os.path.join(BASE_DIR, "test_files", "audio", "potter_to_hermine.wav")


def test_transcribe():
    genai = incredibly_fast_whisper(api_key=os.getenv("SOCAITY_API_KEY", None))
    fj = genai(audio=INPUT_AUDIO)
    generated_text = fj.get_result()
    print(generated_text)
    return generated_text


if __name__ == "__main__":
    test_transcribe()
