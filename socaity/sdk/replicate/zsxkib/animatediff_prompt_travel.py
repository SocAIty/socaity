from fastsdk.fastSDK import FastSDK

class animatediff_prompt_travel(FastSDK):
    """
    Generated client for zsxkib/animatediff-prompt-travel
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="e2029a8e-e0c7-410a-a567-74f77bf16a74", api_key=api_key)
    
    def predict(self, seed: int = -1, steps: int = 25, width: int = 256, frames: int = 128, height: int = 384, context: int = 16, clip_skip: int = 2, scheduler: str = 'k_dpmpp_sde', base_model: str = 'majicmixRealistic_v5Preview', prompt_map: str = '0: ship steadily moving,((waves crashing against the ship:1.0)) | 32: (((lightning strikes))), distant thunder, ship rocked by waves | 64: ship silhouette,(((heavy rain))),wind howling, waves rising higher | 96: ship navigating through the storm, rain easing off', head_prompt: str = 'masterpiece, best quality, a haunting and detailed depiction of a ship at sea, battered by waves, ominous,((dark clouds:1.3)),distant lightning, rough seas, rain, silhouette of the ship against the stormy sky', tail_prompt: str = "dark horizon, flashes of lightning illuminating the ship, sailors working hard, ship's lanterns flickering, eerie, mysterious, sails flapping loudly, stormy atmosphere", output_format: str = 'mp4', guidance_scale: float = 7.5, negative_prompt: str = '(worst quality, low quality:1.4), black and white, b&w, sunny, clear skies, calm seas, beach, daytime, ((bright colors)), cartoonish, modern ships, sketchy, unfinished, modern buildings, trees, island', prompt_fixed_ratio: float = 0.5, custom_base_model_url: str = '', playback_frames_per_second: int = 8, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            seed: Seed for different images and reproducibility. Use -1 to randomise seed Defaults to -1.
            
            steps: Number of inference steps Defaults to 25.
            
            width: Width of generated video in pixels, must be divisable by 8 Defaults to 256.
            
            frames: Length of the video in frames (playback is at 8 fps e.g. 16 frames @ 8 fps is 2 seconds) Defaults to 128.
            
            height: Height of generated video in pixels, must be divisable by 8 Defaults to 384.
            
            context: Number of frames to condition on (default: max of <length> or 32). max for motion module v1 is 24 Defaults to 16.
            
            clip_skip: Skip the last N-1 layers of the CLIP text encoder (lower values follow prompt more closely) Defaults to 2.
            
            scheduler: Diffusion scheduler Defaults to 'k_dpmpp_sde'.
            
            base_model: Choose the base model for animation generation. If 'CUSTOM' is selected, provide a custom model URL in the next parameter Defaults to 'majicmixRealistic_v5Preview'.
            
            prompt_map: Prompt for changes in animation. Provide 'frame number : prompt at this frame', separate different prompts with '|'. Make sure the frame number does not exceed the length of video (frames) Defaults to '0: ship steadily moving,((waves crashing against the ship:1.0)) | 32: (((lightning strikes))), distant thunder, ship rocked by waves | 64: ship silhouette,(((heavy rain))),wind howling, waves rising higher | 96: ship navigating through the storm, rain easing off'.
            
            head_prompt: Primary animation prompt. If a prompt map is provided, this will be prefixed at the start of every individual prompt in the map Defaults to 'masterpiece, best quality, a haunting and detailed depiction of a ship at sea, battered by waves, ominous,((dark clouds:1.3)),distant lightning, rough seas, rain, silhouette of the ship against the stormy sky'.
            
            tail_prompt: Additional prompt that will be appended at the end of the main prompt or individual prompts in the map Defaults to "dark horizon, flashes of lightning illuminating the ship, sailors working hard, ship's lanterns flickering, eerie, mysterious, sails flapping loudly, stormy atmosphere".
            
            output_format: Output format of the video. Can be 'mp4' or 'gif' Defaults to 'mp4'.
            
            guidance_scale: Guidance Scale. How closely do we want to adhere to the prompt and its contents Defaults to 7.5.
            
            negative_prompt: negative_prompt Defaults to '(worst quality, low quality:1.4), black and white, b&w, sunny, clear skies, calm seas, beach, daytime, ((bright colors)), cartoonish, modern ships, sketchy, unfinished, modern buildings, trees, island'.
            
            prompt_fixed_ratio: Defines the ratio of adherence to the fixed part of the prompt versus the dynamic part (from prompt map). Value should be between 0 (only dynamic) to 1 (only fixed). Defaults to 0.5.
            
            custom_base_model_url: Only used when base model is set to 'CUSTOM'. URL of the custom model to download if 'CUSTOM' is selected in the base model. Only downloads from 'https://civitai.com/api/download/models/' are allowed Defaults to ''.
            
            playback_frames_per_second: playback_frames_per_second Defaults to 8.
            
        """
        return self.submit_job("/predictions", seed=seed, steps=steps, width=width, frames=frames, height=height, context=context, clip_skip=clip_skip, scheduler=scheduler, base_model=base_model, prompt_map=prompt_map, head_prompt=head_prompt, tail_prompt=tail_prompt, output_format=output_format, guidance_scale=guidance_scale, negative_prompt=negative_prompt, prompt_fixed_ratio=prompt_fixed_ratio, custom_base_model_url=custom_base_model_url, playback_frames_per_second=playback_frames_per_second, **kwargs)
     