# Examples and Use-Cases

The future of the Internet and the economy is generative. However, there's not one model that fits all.
For real world applications, you need to chain different models together combine them with other services.

AI NPC Agents - How to:
Here's a common example of a game developer who wants to have AI NPC agents in his game. His workflow:
1. Generate the text the NPC should say.
2. use a `text2speech` model to synthesize speech for the NPC.
3. uses the `voice2voice` model to change the voice of the NPC to one of his artists. 
4. uses `audio2face` model to generate facial animations for the NPC.

Automated video content - How to:
1. Create a thumbnail for a video with `text2image`
2. Swap the faces in the video with `face2face`
3. Generate a voice-over for the video with `text2voice`

