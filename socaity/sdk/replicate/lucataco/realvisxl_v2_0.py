from fastsdk.fastSDK import FastSDK
from typing import Optional, Union

from media_toolkit import MediaFile


class realvisxl_v2_0(FastSDK):
    """
    Generated client for realvisxl_v2_0
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="ae83f2c8-4004-4231-b6e7-8582052822dd", api_key=api_key)
    
    def predict(self, width: int = 1024, height: int = 1024, prompt: str = 'dark shot, front shot, closeup photo of a 25 y.o latino man, perfect eyes, natural skin, skin moles, looks at viewer, cinematic shot', scheduler: str = 'DPMSolverMultistep', lora_scale: float = 0.6, num_outputs: int = 1, guidance_scale: float = 7.0, apply_watermark: bool = True, negative_prompt: str = '(worst quality, low quality, illustration, 3d, 2d, painting, cartoons, sketch), open mouth', prompt_strength: float = 0.8, num_inference_steps: int = 40, disable_safety_checker: bool = False, mask: Optional[Union[MediaFile, str, bytes]] = None, seed: Optional[int] = None, image: Optional[Union[MediaFile, str, bytes]] = None, lora_weights: Optional[str] = None, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            width: Width of output image Defaults to 1024.
            
            height: Height of output image Defaults to 1024.
            
            prompt: Input prompt Defaults to 'dark shot, front shot, closeup photo of a 25 y.o latino man, perfect eyes, natural skin, skin moles, looks at viewer, cinematic shot'.
            
            scheduler: scheduler Defaults to 'DPMSolverMultistep'.
            
            lora_scale: LoRA additive scale. Only applicable on trained models. Defaults to 0.6.
            
            num_outputs: Number of images to output. Defaults to 1.
            
            guidance_scale: Scale for classifier-free guidance Defaults to 7.0.
            
            apply_watermark: Applies a watermark to enable determining if an image is generated in downstream applications. If you have other provisions for generating or deploying images safely, you can use this to disable watermarking. Defaults to True.
            
            negative_prompt: Negative Input prompt Defaults to '(worst quality, low quality, illustration, 3d, 2d, painting, cartoons, sketch), open mouth'.
            
            prompt_strength: Prompt strength when using img2img / inpaint. 1.0 corresponds to full destruction of information in image Defaults to 0.8.
            
            num_inference_steps: Number of denoising steps Defaults to 40.
            
            disable_safety_checker: Disable safety checker for generated images. This feature is only available through the API. See https://replicate.com/docs/how-does-replicate-work#safety Defaults to False.
            
            mask: Input mask for inpaint mode. Black areas will be preserved, white areas will be inpainted. Optional.
            
            seed: Random seed. Leave blank to randomize the seed Optional.
            
            image: Input image for img2img or inpaint mode Optional.
            
            lora_weights: Replicate LoRA weights to use. Leave blank to use the default weights. Optional.
            
        """
        return self.submit_job("/predict", width=width, height=height, prompt=prompt, scheduler=scheduler, lora_scale=lora_scale, num_outputs=num_outputs, guidance_scale=guidance_scale, apply_watermark=apply_watermark, negative_prompt=negative_prompt, prompt_strength=prompt_strength, num_inference_steps=num_inference_steps, disable_safety_checker=disable_safety_checker, mask=mask, seed=seed, image=image, lora_weights=lora_weights, **kwargs)
     