from fastsdk import FastSDK, APISeex
from typing import Optional, Union

from media_toolkit import MediaFile


class realvisxl_v4_0(FastSDK):
    """
    Generated client for adirik/realvisxl-v4-0
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="c20d0141-0b72-4529-b504-12d4e3001bd1", api_key=api_key)
    
    def predictions(self, width: int = 768, height: int = 768, prompt: str = 'An astronaut riding a rainbow unicorn', refine: str = 'no_refiner', scheduler: str = 'DPM++_SDE_Karras', num_outputs: int = 1, guidance_scale: float = 4.0, apply_watermark: bool = False, high_noise_frac: float = 0.8, negative_prompt: str = '(worst quality, low quality, illustration, 3d, 2d, painting, cartoons, sketch), open mouth', prompt_strength: float = 0.8, num_inference_steps: int = 25, disable_safety_checker: bool = False, mask: Optional[Union[str, MediaFile, bytes]] = None, seed: Optional[int] = None, image: Optional[Union[str, MediaFile, bytes]] = None, refine_steps: Optional[int] = None, **kwargs) -> APISeex:
        """
        
        
        
        Args:
            width: Width of output image Defaults to 768.
            
            height: Height of output image Defaults to 768.
            
            prompt: Input prompt Defaults to 'An astronaut riding a rainbow unicorn'.
            
            refine: Which refine style to use Defaults to 'no_refiner'.
            
            scheduler: Scheduler to use, DPM++ SDE Karras is recommended Defaults to 'DPM++_SDE_Karras'.
            
            num_outputs: Number of images to output. Defaults to 1.
            
            guidance_scale: Scale for classifier-free guidance Defaults to 4.0.
            
            apply_watermark: Applies a watermark to enable determining if an image is generated in downstream applications. If you have other provisions for generating or deploying images safely, you can use this to disable watermarking. Defaults to False.
            
            high_noise_frac: For expert_ensemble_refiner, the fraction of noise to use Defaults to 0.8.
            
            negative_prompt: Input Negative Prompt Defaults to '(worst quality, low quality, illustration, 3d, 2d, painting, cartoons, sketch), open mouth'.
            
            prompt_strength: Prompt strength when using img2img / inpaint. 1.0 corresponds to full destruction of information in image Defaults to 0.8.
            
            num_inference_steps: Number of denoising steps Defaults to 25.
            
            disable_safety_checker: Disable safety checker for generated images. This feature is only available through the API. See [https://replicate.com/docs/how-does-replicate-work#safety](https://replicate.com/docs/how-does-replicate-work#safety) Defaults to False.
            
            mask: Input mask for inpaint mode. Black areas will be preserved, white areas will be inpainted. Optional.
            
            seed: Random seed. Leave blank to randomize the seed Optional.
            
            image: Input image for img2img or inpaint mode Optional.
            
            refine_steps: For base_image_refiner, the number of steps to refine, defaults to num_inference_steps Optional.
            
        """
        return self.submit_job("/predictions", width=width, height=height, prompt=prompt, refine=refine, scheduler=scheduler, num_outputs=num_outputs, guidance_scale=guidance_scale, apply_watermark=apply_watermark, high_noise_frac=high_noise_frac, negative_prompt=negative_prompt, prompt_strength=prompt_strength, num_inference_steps=num_inference_steps, disable_safety_checker=disable_safety_checker, mask=mask, seed=seed, image=image, refine_steps=refine_steps, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions