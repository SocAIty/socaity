from fastsdk import FastSDK, APISeex
from typing import Optional, Union

from media_toolkit import MediaFile


class sdxl_multi_controlnet_lora(FastSDK):
    """
    Generated client for fofr/sdxl-multi-controlnet-lora
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="03cfb258-a96d-4104-8661-57b7cb7b034d", api_key=api_key)
    
    def predictions(self, width: int = 768, height: int = 768, prompt: str = 'An astronaut riding a rainbow unicorn', refine: str = 'no_refiner', scheduler: str = 'K_EULER', lora_scale: float = 0.6, num_outputs: int = 1, controlnet_1: str = 'none', controlnet_2: str = 'none', controlnet_3: str = 'none', guidance_scale: float = 7.5, apply_watermark: bool = True, negative_prompt: str = '', prompt_strength: float = 0.8, sizing_strategy: str = 'width_height', controlnet_1_end: float = 1.0, controlnet_2_end: float = 1.0, controlnet_3_end: float = 1.0, controlnet_1_start: float = 0.0, controlnet_2_start: float = 0.0, controlnet_3_start: float = 0.0, num_inference_steps: int = 30, disable_safety_checker: bool = False, controlnet_1_conditioning_scale: float = 0.75, controlnet_2_conditioning_scale: float = 0.75, controlnet_3_conditioning_scale: float = 0.75, mask: Optional[Union[MediaFile, str, bytes]] = None, seed: Optional[int] = None, image: Optional[Union[MediaFile, str, bytes]] = None, lora_weights: Optional[str] = None, refine_steps: Optional[int] = None, controlnet_1_image: Optional[Union[MediaFile, str, bytes]] = None, controlnet_2_image: Optional[Union[MediaFile, str, bytes]] = None, controlnet_3_image: Optional[Union[MediaFile, str, bytes]] = None, **kwargs) -> APISeex:
        """
        Run a single prediction on the model
        
        
        Args:
            width: Width of output image Defaults to 768.
            
            height: Height of output image Defaults to 768.
            
            prompt: Input prompt Defaults to 'An astronaut riding a rainbow unicorn'.
            
            refine: Which refine style to use Defaults to 'no_refiner'.
            
            scheduler: scheduler Defaults to 'K_EULER'.
            
            lora_scale: LoRA additive scale. Only applicable on trained models. Defaults to 0.6.
            
            num_outputs: Number of images to output Defaults to 1.
            
            controlnet_1: Controlnet Defaults to 'none'.
            
            controlnet_2: Controlnet Defaults to 'none'.
            
            controlnet_3: Controlnet Defaults to 'none'.
            
            guidance_scale: Scale for classifier-free guidance Defaults to 7.5.
            
            apply_watermark: Applies a watermark to enable determining if an image is generated in downstream applications. If you have other provisions for generating or deploying images safely, you can use this to disable watermarking. Defaults to True.
            
            negative_prompt: Negative Prompt Defaults to ''.
            
            prompt_strength: Prompt strength when using img2img / inpaint. 1.0 corresponds to full destruction of information in image Defaults to 0.8.
            
            sizing_strategy: Decide how to resize images – use width/height, resize based on input image or control image Defaults to 'width_height'.
            
            controlnet_1_end: When controlnet conditioning ends Defaults to 1.0.
            
            controlnet_2_end: When controlnet conditioning ends Defaults to 1.0.
            
            controlnet_3_end: When controlnet conditioning ends Defaults to 1.0.
            
            controlnet_1_start: When controlnet conditioning starts Defaults to 0.0.
            
            controlnet_2_start: When controlnet conditioning starts Defaults to 0.0.
            
            controlnet_3_start: When controlnet conditioning starts Defaults to 0.0.
            
            num_inference_steps: Number of denoising steps Defaults to 30.
            
            disable_safety_checker: Disable safety checker for generated images. This feature is only available through the API. See [https://replicate.com/docs/how-does-replicate-work#safety](https://replicate.com/docs/how-does-replicate-work#safety) Defaults to False.
            
            controlnet_1_conditioning_scale: How strong the controlnet conditioning is Defaults to 0.75.
            
            controlnet_2_conditioning_scale: How strong the controlnet conditioning is Defaults to 0.75.
            
            controlnet_3_conditioning_scale: How strong the controlnet conditioning is Defaults to 0.75.
            
            mask: Input mask for inpaint mode. Black areas will be preserved, white areas will be inpainted. Optional.
            
            seed: Random seed. Leave blank to randomize the seed Optional.
            
            image: Input image for img2img or inpaint mode Optional.
            
            lora_weights: Replicate LoRA weights to use. Leave blank to use the default weights. Optional.
            
            refine_steps: For base_image_refiner, the number of steps to refine, defaults to num_inference_steps Optional.
            
            controlnet_1_image: Input image for first controlnet Optional.
            
            controlnet_2_image: Input image for second controlnet Optional.
            
            controlnet_3_image: Input image for third controlnet Optional.
            
        """
        return self.submit_job("/predictions", width=width, height=height, prompt=prompt, refine=refine, scheduler=scheduler, lora_scale=lora_scale, num_outputs=num_outputs, controlnet_1=controlnet_1, controlnet_2=controlnet_2, controlnet_3=controlnet_3, guidance_scale=guidance_scale, apply_watermark=apply_watermark, negative_prompt=negative_prompt, prompt_strength=prompt_strength, sizing_strategy=sizing_strategy, controlnet_1_end=controlnet_1_end, controlnet_2_end=controlnet_2_end, controlnet_3_end=controlnet_3_end, controlnet_1_start=controlnet_1_start, controlnet_2_start=controlnet_2_start, controlnet_3_start=controlnet_3_start, num_inference_steps=num_inference_steps, disable_safety_checker=disable_safety_checker, controlnet_1_conditioning_scale=controlnet_1_conditioning_scale, controlnet_2_conditioning_scale=controlnet_2_conditioning_scale, controlnet_3_conditioning_scale=controlnet_3_conditioning_scale, mask=mask, seed=seed, image=image, lora_weights=lora_weights, refine_steps=refine_steps, controlnet_1_image=controlnet_1_image, controlnet_2_image=controlnet_2_image, controlnet_3_image=controlnet_3_image, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions