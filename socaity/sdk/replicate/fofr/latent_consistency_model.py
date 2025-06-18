from fastsdk import FastSDK, APISeex
from typing import Optional, Union

from media_toolkit import MediaFile


class latent_consistency_model(FastSDK):
    """
    Generated client for fofr/latent-consistency-model
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="257ba909-831f-4c7c-990e-7aee51b68eb1", api_key=api_key)
    
    def predictions(self, width: int = 768, height: int = 768, prompt: str = 'Self-portrait oil painting, a beautiful cyborg with golden hair, 8k', num_images: int = 1, guidance_scale: float = 8.0, archive_outputs: bool = False, prompt_strength: float = 0.8, sizing_strategy: str = 'width/height', lcm_origin_steps: int = 50, canny_low_threshold: float = 100.0, num_inference_steps: int = 8, canny_high_threshold: float = 200.0, control_guidance_end: float = 1.0, control_guidance_start: float = 0.0, disable_safety_checker: bool = False, controlnet_conditioning_scale: float = 2.0, seed: Optional[int] = None, image: Optional[Union[MediaFile, str, bytes]] = None, control_image: Optional[Union[MediaFile, str, bytes]] = None, **kwargs) -> APISeex:
        """
        Run a single prediction on the model
        
        
        Args:
            width: Width of output image. Lower if out of memory Defaults to 768.
            
            height: Height of output image. Lower if out of memory Defaults to 768.
            
            prompt: For multiple prompts, enter each on a new line. Defaults to 'Self-portrait oil painting, a beautiful cyborg with golden hair, 8k'.
            
            num_images: Number of images per prompt Defaults to 1.
            
            guidance_scale: Scale for classifier-free guidance Defaults to 8.0.
            
            archive_outputs: Option to archive the output images Defaults to False.
            
            prompt_strength: Prompt strength when using img2img. 1.0 corresponds to full destruction of information in image Defaults to 0.8.
            
            sizing_strategy: Decide how to resize images – use width/height, resize based on input image or control image Defaults to 'width/height'.
            
            lcm_origin_steps: lcm_origin_steps Defaults to 50.
            
            canny_low_threshold: Canny low threshold Defaults to 100.0.
            
            num_inference_steps: Number of denoising steps. Recommend 1 to 8 steps. Defaults to 8.
            
            canny_high_threshold: Canny high threshold Defaults to 200.0.
            
            control_guidance_end: Controlnet end Defaults to 1.0.
            
            control_guidance_start: Controlnet start Defaults to 0.0.
            
            disable_safety_checker: Disable safety checker for generated images. This feature is only available through the API Defaults to False.
            
            controlnet_conditioning_scale: Controlnet conditioning scale Defaults to 2.0.
            
            seed: Random seed. Leave blank to randomize the seed Optional.
            
            image: Input image for img2img Optional.
            
            control_image: Image for controlnet conditioning Optional.
            
        """
        return self.submit_job("/predictions", width=width, height=height, prompt=prompt, num_images=num_images, guidance_scale=guidance_scale, archive_outputs=archive_outputs, prompt_strength=prompt_strength, sizing_strategy=sizing_strategy, lcm_origin_steps=lcm_origin_steps, canny_low_threshold=canny_low_threshold, num_inference_steps=num_inference_steps, canny_high_threshold=canny_high_threshold, control_guidance_end=control_guidance_end, control_guidance_start=control_guidance_start, disable_safety_checker=disable_safety_checker, controlnet_conditioning_scale=controlnet_conditioning_scale, seed=seed, image=image, control_image=control_image, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions