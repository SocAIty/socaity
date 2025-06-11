import os

from socaity.api.text import InsanelyFastWhisper

test_audio = "test_files/audio/potter_to_hermine.wav"
genai = InsanelyFastWhisper()
# fluxs = FluxSchnell(service="socaity_local", api_key=os.getenv("SOCAITY_API_KEY", None))

def test_transcribe():
    fj = genai.transcribe(audio=test_audio)
    generated_text = fj.get_result()
    print(generated_text)


if __name__ == "__main__":
    test_transcribe()
