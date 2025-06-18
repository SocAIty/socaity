from socaity import speechcraft, MediaFile
import os


# Global directory paths for use in both pytest and direct execution
BASE_DIR = os.path.dirname(__file__)
INPUT_DIR = os.path.join(BASE_DIR, "test_files", "text2speech")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
SAMPLE_TEXT = "I love society [laughs]! [happy] What a day to make voice overs with artificial intelligence."
TEST_FILE_1 = f'{INPUT_DIR}/voice_clone_test_voice_1.wav'
TEST_FILE_2 = f'{INPUT_DIR}/voice_clone_test_voice_2.wav'

os.makedirs(OUTPUT_DIR, exist_ok=True)
speechcraft = speechcraft()


def test_text2voice():
    t2v_job = speechcraft.text2voice(SAMPLE_TEXT)
    audio = t2v_job.get_result()
    output_path = f"{OUTPUT_DIR}/en_speaker_3_i_love_socaity.wav"
    audio.save(output_path)
    assert os.path.exists(output_path), f"Output file {output_path} was not created"


def test_voice2embedding():
    v2e_job = speechcraft.voice2embedding(audio_file=TEST_FILE_1, voice_name="hermine", save=False)
    embedding = v2e_job.get_result()
    assert embedding is not None, "Voice embedding should not be None"
    embedding.save(f"{OUTPUT_DIR}/hermine_embedding.wav")


def test_test2voice_with_embedding():
    if not os.path.exists(f"{OUTPUT_DIR}/hermine_embedding.wav"):
        test_voice2embedding()

    assert os.path.exists(f"{OUTPUT_DIR}/hermine_embedding.wav"), "Voice embedding file should exist"
    voice = MediaFile().from_file(f"{OUTPUT_DIR}/hermine_embedding.wav")
    audio_with_cloned_voice = speechcraft.text2voice(SAMPLE_TEXT, voice=voice).get_result()
    output_path = f"{OUTPUT_DIR}/hermine_i_love_socaity.wav"
    audio_with_cloned_voice.save(output_path)
    assert os.path.exists(output_path), f"Output file {output_path} was not created"


def test_voice2voice():
    v2v_job = speechcraft.voice2voice(audio_file=TEST_FILE_2, voice_name="hermine")
    v2v_audio = v2v_job.get_result()
    assert v2v_audio is not None, "Voice2Voice result should not be None"
    
    output_path = f"{OUTPUT_DIR}/benni.wav"
    v2v_audio.save(output_path)
    assert os.path.exists(output_path), f"Output file {output_path} was not created"


def test_speechcraft_initialization():
    assert speechcraft is not None, "Speechcraft should not be None"
    assert hasattr(speechcraft, 'text2voice'), "Speechcraft should have text2voice method"
    assert hasattr(speechcraft, 'voice2embedding'), "Speechcraft should have voice2embedding method"
    assert hasattr(speechcraft, 'voice2voice'), "Speechcraft should have voice2voice method"


def test_speechcraft():
    test_speechcraft_initialization()
    test_text2voice()
    test_voice2embedding()
    test_test2voice_with_embedding()
    test_voice2voice()
    return True


if __name__ == "__main__":
    # When running directly, fixtures are just regular functions
    # test_voice2embedding()
    test_test2voice_with_embedding()
