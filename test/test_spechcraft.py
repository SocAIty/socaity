from socaity import SpeechCraft

test_file_1 = 'test_files/text2speech/voice_clone_test_voice_1.wav'
test_file_2 = 'test_files/text2speech/voice_clone_test_voice_2.wav'

sample_text = "I love society [laughs]! [happy] What a day to make voice overs with artificial intelligence."


sc = SpeechCraft()
# test text2speech
t2v_job = sc.text2voice(sample_text)
audio = t2v_job.get_result()
#audio.save("en_speaker_3_i_love_socaity.wav")

## test voice cloning
v2e_job = sc.voice2embedding(audio_file=test_file_1, voice_name="hermine2", save=True)
embedding = v2e_job.get_result()
audio_with_cloned_voice = sc.text2voice(sample_text, voice="hermine2").get_result()
audio_with_cloned_voice.save("hermine_i_love_socaity.wav")

# test voice2voice
v2v_job = sc.voice2voice(
    audio_file="test_files/voice_clone_test_voice_2.wav",
    voice_name="hermine2"
)
v2v_audio = v2v_job.get_result()
v2v_audio.save("hermine_to_potter.wav")
a = 1