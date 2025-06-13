from fastsdk.fastSDK import FastSDK
from typing import Union, Optional

from media_toolkit import MediaFile


class playground_v2_5_1024px_aesthetic(FastSDK):
    """
    Generated client for playgroundai/playground-v2-5-1024px-aesthetic
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="98466e47-f0f6-4cfe-8842-f7758bd9d61c", api_key=api_key)
    
    def predict(self, width: int = 1024, height: int = 1024, prompt: str = 'Astronaut in a jungle, cold color palette, muted colors, detailed, 8k', scheduler: str = 'DPMSolver++', num_outputs: int = 1, guidance_scale: float = 3.0, apply_watermark: bool = True, negative_prompt: str = 'ugly, deformed, noisy, blurry, distorted', prompt_strength: float = 0.8, num_inference_steps: int = 25, disable_safety_checker: bool = False, mask: Optional[Union[MediaFile, str, bytes]] = None, seed: Optional[int] = None, image: Optional[Union[MediaFile, str, bytes]] = None, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            width: Width of output image Defaults to 1024.
            
            height: Height of output image Defaults to 1024.
            
            prompt: Input prompt Defaults to 'Astronaut in a jungle, cold color palette, muted colors, detailed, 8k'.
            
            scheduler: Scheduler. DPMSolver++ or DPM++2MKarras is recommended for most cases Defaults to 'DPMSolver++'.
            
            num_outputs: Number of images to output. Defaults to 1.
            
            guidance_scale: Scale for classifier-free guidance Defaults to 3.0.
            
            apply_watermark: Applies a watermark to enable determining if an image is generated in downstream applications. If you have other provisions for generating or deploying images safely, you can use this to disable watermarking. Defaults to True.
            
            negative_prompt: Negative Input prompt Defaults to 'ugly, deformed, noisy, blurry, distorted'.
            
            prompt_strength: Prompt strength when using img2img / inpaint. 1.0 corresponds to full destruction of information in image Defaults to 0.8.
            
            num_inference_steps: Number of denoising steps Defaults to 25.
            
            disable_safety_checker: Disable safety checker for generated images. This feature is only available through the API. See https://replicate.com/docs/how-does-replicate-work#safety Defaults to False.
            
            mask: Input mask for inpaint mode. Black areas will be preserved, white areas will be inpainted. Optional.
            
            seed: Random seed. Leave blank to randomize the seed Optional.
            
            image: Input image for img2img or inpaint mode Optional.
            
        """
        return self.submit_job("/predictions", width=width, height=height, prompt=prompt, scheduler=scheduler, num_outputs=num_outputs, guidance_scale=guidance_scale, apply_watermark=apply_watermark, negative_prompt=negative_prompt, prompt_strength=prompt_strength, num_inference_steps=num_inference_steps, disable_safety_checker=disable_safety_checker, mask=mask, seed=seed, image=image, **kwargs)
     