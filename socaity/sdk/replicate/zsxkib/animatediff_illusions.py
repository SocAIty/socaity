from fastsdk.fastSDK import FastSDK
from typing import Union, Optional

from media_toolkit import MediaFile


class animatediff_illusions(FastSDK):
    """
    Generated client for zsxkib/animatediff-illusions
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="7004e090-b95e-4df1-b93f-0bf02eb1769a", api_key=api_key)
    
    def predict(self, loop: bool = True, steps: int = 25, width: int = 256, frames: int = 128, height: int = 384, context: int = 16, clip_skip: int = 2, scheduler: str = 'k_dpmpp_sde', base_model: str = 'majicmixRealistic_v5Preview', prompt_map: str = '', head_prompt: str = 'masterpiece, best quality, a haunting and detailed depiction of a ship at sea, battered by waves, ominous,((dark clouds:1.3)),distant lightning, rough seas, rain, silhouette of the ship against the stormy sky', tail_prompt: str = '', output_format: str = 'mp4', guidance_scale: float = 7.5, negative_prompt: str = '', film_interpolation: bool = True, prompt_fixed_ratio: float = 0.5, custom_base_model_url: str = '', num_interpolation_steps: int = 3, enable_qr_code_monster_v2: bool = True, playback_frames_per_second: int = 8, controlnet_conditioning_scale: float = 0.18, qr_code_monster_v2_guess_mode: bool = False, qr_code_monster_v2_preprocessor: bool = True, seed: Optional[int] = None, controlnet_video: Optional[Union[MediaFile, str, bytes]] = None, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            loop: Flag to loop the video. Use when you have an 'infinitely' repeating video/gif ControlNet video Defaults to True.
            
            steps: Number of inference steps Defaults to 25.
            
            width: Width of generated video in pixels, must be divisable by 8 Defaults to 256.
            
            frames: Length of the video in frames (playback is at 8 fps e.g. 16 frames @ 8 fps is 2 seconds) Defaults to 128.
            
            height: Height of generated video in pixels, must be divisable by 8 Defaults to 384.
            
            context: Number of frames to condition on (default: max of <length> or 32). max for motion module v1 is 24 Defaults to 16.
            
            clip_skip: Skip the last N-1 layers of the CLIP text encoder (lower values follow prompt more closely) Defaults to 2.
            
            scheduler: Diffusion scheduler Defaults to 'k_dpmpp_sde'.
            
            base_model: Choose the base model for animation generation. If 'CUSTOM' is selected, provide a custom model URL in the next parameter Defaults to 'majicmixRealistic_v5Preview'.
            
            prompt_map: Prompt for changes in animation. Provide 'frame number : prompt at this frame', separate different prompts with '|'. Make sure the frame number does not exceed the length of video (frames) Defaults to ''.
            
            head_prompt: Primary animation prompt. If a prompt map is provided, this will be prefixed at the start of every individual prompt in the map Defaults to 'masterpiece, best quality, a haunting and detailed depiction of a ship at sea, battered by waves, ominous,((dark clouds:1.3)),distant lightning, rough seas, rain, silhouette of the ship against the stormy sky'.
            
            tail_prompt: Additional prompt that will be appended at the end of the main prompt or individual prompts in the map Defaults to ''.
            
            output_format: Output format of the video. Can be 'mp4' or 'gif' Defaults to 'mp4'.
            
            guidance_scale: Guidance Scale. How closely do we want to adhere to the prompt and its contents Defaults to 7.5.
            
            negative_prompt: negative_prompt Defaults to ''.
            
            film_interpolation: Whether to use FILM for between-frame interpolation (film-net.github.io) Defaults to True.
            
            prompt_fixed_ratio: Defines the ratio of adherence to the fixed part of the prompt versus the dynamic part (from prompt map). Value should be between 0 (only dynamic) to 1 (only fixed). Defaults to 0.5.
            
            custom_base_model_url: Only used when base model is set to 'CUSTOM'. URL of the custom model to download if 'CUSTOM' is selected in the base model. Only downloads from 'https://civitai.com/api/download/models/' are allowed Defaults to ''.
            
            num_interpolation_steps: Number of steps to interpolate between animation frames Defaults to 3.
            
            enable_qr_code_monster_v2: Flag to enable QR Code Monster V2 ControlNet Defaults to True.
            
            playback_frames_per_second: playback_frames_per_second Defaults to 8.
            
            controlnet_conditioning_scale: Strength of ControlNet. The outputs of the ControlNet are multiplied by `controlnet_conditioning_scale` before they are added to the residual in the original UNet Defaults to 0.18.
            
            qr_code_monster_v2_guess_mode: Flag to enable guess mode (un-guided) for QR Code Monster V2 ControlNet Defaults to False.
            
            qr_code_monster_v2_preprocessor: Flag to pre-process keyframes for QR Code Monster V2 ControlNet Defaults to True.
            
            seed: Seed for different images and reproducibility. Leave blank to randomise seed Optional.
            
            controlnet_video: A short video/gif that will be used as the keyframes for QR Code Monster to use, Please note, all of the frames will be used as keyframes Optional.
            
        """
        return self.submit_job("/predictions", loop=loop, steps=steps, width=width, frames=frames, height=height, context=context, clip_skip=clip_skip, scheduler=scheduler, base_model=base_model, prompt_map=prompt_map, head_prompt=head_prompt, tail_prompt=tail_prompt, output_format=output_format, guidance_scale=guidance_scale, negative_prompt=negative_prompt, film_interpolation=film_interpolation, prompt_fixed_ratio=prompt_fixed_ratio, custom_base_model_url=custom_base_model_url, num_interpolation_steps=num_interpolation_steps, enable_qr_code_monster_v2=enable_qr_code_monster_v2, playback_frames_per_second=playback_frames_per_second, controlnet_conditioning_scale=controlnet_conditioning_scale, qr_code_monster_v2_guess_mode=qr_code_monster_v2_guess_mode, qr_code_monster_v2_preprocessor=qr_code_monster_v2_preprocessor, seed=seed, controlnet_video=controlnet_video, **kwargs)
     