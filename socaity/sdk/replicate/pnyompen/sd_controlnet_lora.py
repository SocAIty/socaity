from fastsdk import FastSDK, APISeex
from typing import Optional, Union

from media_toolkit import MediaFile


class sd_controlnet_lora(FastSDK):
    """
    Generated client for pnyompen/sd-controlnet-lora
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="1f2089d2-a406-4fd6-b762-496d74794321", api_key=api_key)
    
    def predictions(self, prompt: str = 'An astronaut riding a rainbow unicorn', img2img: bool = False, strength: float = 0.8, remove_bg: bool = False, scheduler: str = 'K_EULER', lora_scale: float = 0.95, num_outputs: int = 1, guidance_scale: float = 7.5, condition_scale: float = 1.1, negative_prompt: str = '', ip_adapter_scale: float = 1.0, num_inference_steps: int = 30, auto_generate_caption: bool = False, generated_caption_weight: float = 0.5, seed: Optional[int] = None, image: Optional[Union[str, MediaFile, bytes]] = None, lora_weights: Optional[str] = None, **kwargs) -> APISeex:
        """
        
        
        
        Args:
            prompt: Input prompt Defaults to 'An astronaut riding a rainbow unicorn'.
            
            img2img: Use img2img pipeline, it will use the image input both as the control image and the base image. Defaults to False.
            
            strength: When img2img is active, the denoising strength. 1 means total destruction of the input image. Defaults to 0.8.
            
            remove_bg: Remove background from the input image Defaults to False.
            
            scheduler: scheduler Defaults to 'K_EULER'.
            
            lora_scale: LoRA additive scale. Only applicable on trained models. Defaults to 0.95.
            
            num_outputs: Number of images to output Defaults to 1.
            
            guidance_scale: Scale for classifier-free guidance Defaults to 7.5.
            
            condition_scale: The bigger this number is, the more ControlNet interferes Defaults to 1.1.
            
            negative_prompt: Input Negative Prompt Defaults to ''.
            
            ip_adapter_scale: Scale for the IP Adapter Defaults to 1.0.
            
            num_inference_steps: Number of denoising steps Defaults to 30.
            
            auto_generate_caption: Use BLIP to generate captions for the input images Defaults to False.
            
            generated_caption_weight: Weight for the generated caption Defaults to 0.5.
            
            seed: Random seed. Leave blank to randomize the seed Optional.
            
            image: Input image for img2img or inpaint mode Optional.
            
            lora_weights: Replicate LoRA weights to use. Leave blank to use the default weights. Optional.
            
        """
        return self.submit_job("/predictions", prompt=prompt, img2img=img2img, strength=strength, remove_bg=remove_bg, scheduler=scheduler, lora_scale=lora_scale, num_outputs=num_outputs, guidance_scale=guidance_scale, condition_scale=condition_scale, negative_prompt=negative_prompt, ip_adapter_scale=ip_adapter_scale, num_inference_steps=num_inference_steps, auto_generate_caption=auto_generate_caption, generated_caption_weight=generated_caption_weight, seed=seed, image=image, lora_weights=lora_weights, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions