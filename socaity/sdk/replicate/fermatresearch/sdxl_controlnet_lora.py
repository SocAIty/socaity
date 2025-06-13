from fastsdk.fastSDK import FastSDK
from typing import Union, Optional

from media_toolkit import MediaFile


class sdxl_controlnet_lora(FastSDK):
    """
    Generated client for fermatresearch/sdxl-controlnet-lora
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="1b81bbd8-39b8-4955-add4-8e5265beb41b", api_key=api_key)
    
    def predict(self, prompt: str = 'An astronaut riding a rainbow unicorn', refine: str = 'base_image_refiner', strength: float = 0.8, scheduler: str = 'K_EULER', lora_scale: float = 0.95, num_outputs: int = 1, refine_steps: int = 10, guidance_scale: float = 7.5, apply_watermark: bool = True, condition_scale: float = 1.1, negative_prompt: str = '', num_inference_steps: int = 30, seed: Optional[int] = None, image: Optional[Union[MediaFile, str, bytes]] = None, img2img: Optional[bool] = None, lora_weights: Optional[str] = None, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            prompt: Input prompt Defaults to 'An astronaut riding a rainbow unicorn'.
            
            refine: Whether to use refinement steps or not Defaults to 'base_image_refiner'.
            
            strength: When img2img is active, the denoising strength. 1 means total destruction of the input image. Defaults to 0.8.
            
            scheduler: scheduler Defaults to 'K_EULER'.
            
            lora_scale: LoRA additive scale. Only applicable on trained models. Defaults to 0.95.
            
            num_outputs: Number of images to output Defaults to 1.
            
            refine_steps: For base_image_refiner, the number of steps to refine Defaults to 10.
            
            guidance_scale: Scale for classifier-free guidance Defaults to 7.5.
            
            apply_watermark: Applies a watermark to enable determining if an image is generated in downstream applications. If you have other provisions for generating or deploying images safely, you can use this to disable watermarking. Defaults to True.
            
            condition_scale: The bigger this number is, the more ControlNet interferes Defaults to 1.1.
            
            negative_prompt: Input Negative Prompt Defaults to ''.
            
            num_inference_steps: Number of denoising steps Defaults to 30.
            
            seed: Random seed. Leave blank to randomize the seed Optional.
            
            image: Input image for img2img or inpaint mode Optional.
            
            img2img: Use img2img pipeline, it will use the image input both as the control image and the base image. Optional.
            
            lora_weights: Replicate LoRA weights to use. Leave blank to use the default weights. Optional.
            
        """
        return self.submit_job("/predictions", prompt=prompt, refine=refine, strength=strength, scheduler=scheduler, lora_scale=lora_scale, num_outputs=num_outputs, refine_steps=refine_steps, guidance_scale=guidance_scale, apply_watermark=apply_watermark, condition_scale=condition_scale, negative_prompt=negative_prompt, num_inference_steps=num_inference_steps, seed=seed, image=image, img2img=img2img, lora_weights=lora_weights, **kwargs)
     