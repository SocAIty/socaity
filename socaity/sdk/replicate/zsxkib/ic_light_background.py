from fastsdk import FastSDK, APISeex
from typing import Optional, Union

from media_toolkit import MediaFile


class ic_light_background(FastSDK):
    """
    Generated client for zsxkib/ic-light-background
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="1fb36653-7ac0-4755-8d93-af13540a00eb", api_key=api_key)
    
    def predictions(self, prompt: str, subject_image: Union[str, MediaFile, bytes], background_image: Union[str, MediaFile, bytes], cfg: float = 2.0, steps: int = 25, width: int = 512, height: int = 640, light_source: str = 'Use Background Image', highres_scale: float = 1.5, output_format: str = 'webp', compute_normal: bool = False, output_quality: int = 80, appended_prompt: str = 'best quality', highres_denoise: float = 0.5, negative_prompt: str = 'lowres, bad anatomy, bad hands, cropped, worst quality', number_of_images: int = 1, seed: Optional[int] = None, **kwargs) -> APISeex:
        """
        
        
        
        Args:
            prompt: A text description guiding the relighting and generation process
            
            subject_image: The main foreground image to be relighted
            
            background_image: The background image that will be used to relight the main foreground image
            
            cfg: Classifier-Free Guidance scale - higher values encourage adherence to prompt, lower values encourage more creative interpretation Defaults to 2.0.
            
            steps: The number of diffusion steps to perform during generation (more steps generally improves image quality but increases processing time) Defaults to 25.
            
            width: The width of the generated images in pixels Defaults to 512.
            
            height: The height of the generated images in pixels Defaults to 640.
            
            light_source: The type and position of lighting to apply to the initial background latent Defaults to 'Use Background Image'.
            
            highres_scale: The multiplier for the final output resolution relative to the initial latent resolution Defaults to 1.5.
            
            output_format: The image file format of the generated output images Defaults to 'webp'.
            
            compute_normal: Whether to compute the normal maps (slower but provides additional output images) Defaults to False.
            
            output_quality: The image compression quality (for lossy formats like JPEG and WebP). 100 = best quality, 0 = lowest quality. Defaults to 80.
            
            appended_prompt: Additional text to be appended to the main prompt, enhancing image quality Defaults to 'best quality'.
            
            highres_denoise: Controls the amount of denoising applied when refining the high resolution output (higher = more adherence to the upscaled latent, lower = more creative details added) Defaults to 0.5.
            
            negative_prompt: A text description of attributes to avoid in the generated images Defaults to 'lowres, bad anatomy, bad hands, cropped, worst quality'.
            
            number_of_images: The number of unique images to generate from the given input and settings Defaults to 1.
            
            seed: A fixed random seed for reproducible results (omit this parameter for a randomized seed) Optional.
            
        """
        return self.submit_job("/predictions", prompt=prompt, subject_image=subject_image, background_image=background_image, cfg=cfg, steps=steps, width=width, height=height, light_source=light_source, highres_scale=highres_scale, output_format=output_format, compute_normal=compute_normal, output_quality=output_quality, appended_prompt=appended_prompt, highres_denoise=highres_denoise, negative_prompt=negative_prompt, number_of_images=number_of_images, seed=seed, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions