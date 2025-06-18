from fastsdk import FastSDK, APISeex
from typing import Optional, Union

from media_toolkit import MediaFile


class stable_diffusion_dance(FastSDK):
    """
    Generated client for pollinations/stable-diffusion-dance
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="35430f6b-5b5a-45c2-adf9-6830a2f707ac", api_key=api_key)
    
    def predictions(self, width: int = 384, height: int = 512, prompts: str = 'a moth\na killer dragonfly\nTwo fishes talking to eachother in deep sea', batch_size: int = 24, frame_rate: float = 16.0, random_seed: int = 13, prompt_scale: float = 15.0, style_suffix: str = 'Painting by Paul Klee, intricate details', audio_smoothing: float = 0.8, diffusion_steps: int = 20, audio_noise_scale: float = 0.3, audio_loudness_type: str = 'peak', frame_interpolation: bool = True, audio_file: Optional[Union[MediaFile, str, bytes]] = None, **kwargs) -> APISeex:
        """
        Run a single prediction on the model
        
        
        Args:
            width: Width of the generated image. The model was really only trained on 512x512 images. Other sizes tend to create less coherent images. Defaults to 384.
            
            height: Height of the generated image. The model was really only trained on 512x512 images. Other sizes tend to create less coherent images. Defaults to 512.
            
            prompts: prompts Defaults to 'a moth\na killer dragonfly\nTwo fishes talking to eachother in deep sea'.
            
            batch_size: Number of images to generate at once. Higher batch sizes will generate images faster but will use more GPU memory i.e. not work depending on resolution. Defaults to 24.
            
            frame_rate: Frames per second for the generated video. Defaults to 16.0.
            
            random_seed: Each seed generates a different image Defaults to 13.
            
            prompt_scale: Determines influence of your prompt on generation. Defaults to 15.0.
            
            style_suffix: Style suffix to add to the prompt. This can be used to add the same style to each prompt. Defaults to 'Painting by Paul Klee, intricate details'.
            
            audio_smoothing: Audio smoothing factor. Defaults to 0.8.
            
            diffusion_steps: Number of diffusion steps. Higher steps could produce better results but will take longer to generate. Maximum 30 (using K-Euler-Diffusion). Defaults to 20.
            
            audio_noise_scale: Larger values mean audio will lead to bigger changes in the image. Defaults to 0.3.
            
            audio_loudness_type: Type of loudness to use for audio. Options are 'rms' or 'peak'. Defaults to 'peak'.
            
            frame_interpolation: Whether to interpolate between frames using FFMPEG or not. Defaults to True.
            
            audio_file: input audio file Optional.
            
        """
        return self.submit_job("/predictions", width=width, height=height, prompts=prompts, batch_size=batch_size, frame_rate=frame_rate, random_seed=random_seed, prompt_scale=prompt_scale, style_suffix=style_suffix, audio_smoothing=audio_smoothing, diffusion_steps=diffusion_steps, audio_noise_scale=audio_noise_scale, audio_loudness_type=audio_loudness_type, frame_interpolation=frame_interpolation, audio_file=audio_file, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions