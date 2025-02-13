from socaity import SpeechCraft
import os

test_file_1 = 'test_files/text2speech/voice_clone_test_voice_1.wav'
test_file_2 = 'test_files/text2speech/voice_clone_test_voice_2.wav'

sample_text = "I love socaity [laughs]. What a time to be alive"
out_dir = "test_files/output/text2speech"

sc = SpeechCraft()

def test_text2voice():
    t2v_job = sc.text2voice(sample_text)
    audio = t2v_job.get_result()
    audio.save(f"{out_dir}/en_speaker_3_i_love_socaity.wav")


## test voice cloning
def test_voice2embedding():
    v2e_job = sc.voice2embedding(audio_file=test_file_1, voice_name="hermine", save=True)
    embedding = v2e_job.get_result()
    audio_with_cloned_voice = sc.text2voice(sample_text, voice=embedding).get_result()
    audio_with_cloned_voice.save(f"{out_dir}/hermine_i_love_socaity.wav")

def test_voice2voice():
    # test voice2voice
    v2v_job = sc.voice2voice(
        audio_file=test_file_2,
        voice_name="hermine"
    )
    v2v_audio = v2v_job.get_result()
    v2v_audio.save(f"{out_dir}/benni.wav")



if __name__ == "__main__":
    test_text2voice()
    test_voice2embedding()
    test_voice2voice()
