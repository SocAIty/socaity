import os
from socaity.sdk.replicate.tencent import hunyuan_video


def test_text2video():
    genai = hunyuan_video(api_key=os.getenv("SOCAITY_API_KEY", None))

    prompt = (
        "Rick (of Rick and Morty) sells a GPU over the counter in a computer store."
        "Rick is standing behind the counter. He already has the GPU in his hand and is not moving within the store."
        "The counter is a designer piece and has the shape of an cloud. "
        "The beginning of the scene is a medium-shot having Rick and the counter in focus."
        "Rick hands over an NVIDIA GPU into the camera."
        "While doing so, the camera quickly zooms-in to a close-up shot of the GPU."
        "Text on the GPU is SOCAITY. "
        "The store if full of shelf with GPUs, RAMs and servers."
        "The store is dark-lit in neon deep-purple light. "
        "One ambient spot-light is over the desk. "
        "The furniture design is in vibrant neon-green lime colors."
        "Sci-fi. Cyberpunk neon-punk. 4k. Cinematic. "
        "Filmed by Robert Zemeckis, Baz Luhrmann, Gerry Anderson"
    )
    fj = genai.text2video(text=prompt, width=512, height=512, video_length=97)
    vid = fj.get_result()
    vid = [vid] if not isinstance(vid, list) else vid
    for i, v in enumerate(vid):
        v.save(f"test_files/output/text2video/test_hunyuan_video_{i+1}.mp4")


if __name__ == "__main__":
    test_text2video()