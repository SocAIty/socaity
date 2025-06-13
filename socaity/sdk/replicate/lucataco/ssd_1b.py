from fastsdk.fastSDK import FastSDK
from typing import Union, Optional

from media_toolkit import MediaFile


class ssd_1b(FastSDK):
    """
    Generated client for lucataco/ssd-1b
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="7fe791ac-9587-4813-9c0d-857e2ecfbf47", api_key=api_key)
    
    def predict(self, width: int = 768, height: int = 768, prompt: str = 'with smoke, half ice and half fire and ultra realistic in detail.wolf, typography, dark fantasy, wildlife photography, vibrant, cinematic and on a black background', scheduler: str = 'K_EULER', lora_scale: float = 0.6, num_outputs: int = 1, batched_prompt: bool = False, guidance_scale: float = 7.5, apply_watermark: bool = True, negative_prompt: str = 'scary, cartoon, painting', prompt_strength: float = 0.8, num_inference_steps: int = 25, disable_safety_checker: bool = False, mask: Optional[Union[MediaFile, str, bytes]] = None, seed: Optional[int] = None, image: Optional[Union[MediaFile, str, bytes]] = None, replicate_weights: Optional[str] = None, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            width: Width of output image Defaults to 768.
            
            height: Height of output image Defaults to 768.
            
            prompt: Input prompt Defaults to 'with smoke, half ice and half fire and ultra realistic in detail.wolf, typography, dark fantasy, wildlife photography, vibrant, cinematic and on a black background'.
            
            scheduler: scheduler Defaults to 'K_EULER'.
            
            lora_scale: LoRA additive scale. Only applicable on trained models. Defaults to 0.6.
            
            num_outputs: Number of images to output. Defaults to 1.
            
            batched_prompt: When active, your prompt will be split by newlines and images will be generated for each individual line Defaults to False.
            
            guidance_scale: Scale for classifier-free guidance Defaults to 7.5.
            
            apply_watermark: Applies a watermark to enable determining if an image is generated in downstream applications. If you have other provisions for generating or deploying images safely, you can use this to disable watermarking. Defaults to True.
            
            negative_prompt: Negative Input prompt Defaults to 'scary, cartoon, painting'.
            
            prompt_strength: Prompt strength when using img2img / inpaint. 1.0 corresponds to full destruction of information in image Defaults to 0.8.
            
            num_inference_steps: Number of denoising steps Defaults to 25.
            
            disable_safety_checker: Disable safety checker for generated images. This feature is only available through the API. See https://replicate.com/docs/how-does-replicate-work#safety Defaults to False.
            
            mask: Input mask for inpaint mode. Black areas will be preserved, white areas will be inpainted. Optional.
            
            seed: Random seed. Leave blank to randomize the seed Optional.
            
            image: Input image for img2img or inpaint mode Optional.
            
            replicate_weights: Replicate LoRA weights to use. Leave blank to use the default weights. Optional.
            
        """
        return self.submit_job("/predictions", width=width, height=height, prompt=prompt, scheduler=scheduler, lora_scale=lora_scale, num_outputs=num_outputs, batched_prompt=batched_prompt, guidance_scale=guidance_scale, apply_watermark=apply_watermark, negative_prompt=negative_prompt, prompt_strength=prompt_strength, num_inference_steps=num_inference_steps, disable_safety_checker=disable_safety_checker, mask=mask, seed=seed, image=image, replicate_weights=replicate_weights, **kwargs)
     