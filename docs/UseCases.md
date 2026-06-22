# Examples and use cases

Most real applications chain a few models together. With `socaity.run` each step is a single call, so a whole pipeline stays readable.

## Narrated explainer

Write the script with an LLM, generate a cover image, and synthesize a voiceover. Three calls, three models:

```python
import socaity

script = "".join(str(chunk) for chunk in socaity.run(
    "deepseek-ai/deepseek-v3",
    prompt="Write two sentences explaining serverless GPU hosting.",
))

cover = socaity.run("black-forest-labs/flux-schnell", prompt="abstract lime on black, minimal")
voice = socaity.run("jaaari/kokoro-82m", text=script, voice="af_bella")

cover.save("cover.png")
voice.save("voiceover.wav")
```

`socaity.run` reads your `SOCAITY_API_KEY` from the environment and returns a typed result per model: text chunks from the LLM, an `ImageFile` from flux, an `AudioFile` from kokoro.

Pick any of the 441 models at [socaity.ai](https://www.socaity.ai) and pass its inputs the same way.
