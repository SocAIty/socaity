from fastsdk.fastSDK import FastSDK
from typing import Union, Optional

from media_toolkit import MediaFile


class controlnet_x_ip_adapter_realistic_vision_v5(FastSDK):
    """
    Generated client for usamaehsan/controlnet-x-ip-adapter-realistic-vision-v5
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="9a2ea88f-8dd0-4642-bc51-91bce767cdf0", api_key=api_key)
    
    def predict(self, prompt: str, eta: float = 0.0, max_width: int = 512, scheduler: str = 'DDIM', guess_mode: bool = False, int_kwargs: str = '', max_height: int = 512, num_outputs: int = 1, guidance_scale: float = 7.0, ip_adapter_ckpt: str = 'ip-adapter_sd15.bin', negative_prompt: str = 'Longbody, lowres, bad anatomy, bad hands, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality', img2img_strength: float = 0.5, ip_adapter_weight: float = 1.0, sorted_controlnets: str = 'lineart, tile, inpainting', inpainting_strength: float = 1.0, num_inference_steps: int = 20, disable_safety_check: bool = False, film_grain_lora_weight: float = 0.0, tile_conditioning_scale: float = 1.0, add_more_detail_lora_scale: float = 0.5, detail_tweaker_lora_weight: float = 0.0, lineart_conditioning_scale: float = 1.0, scribble_conditioning_scale: float = 1.0, epi_noise_offset_lora_weight: float = 0.0, brightness_conditioning_scale: float = 1.0, inpainting_conditioning_scale: float = 1.0, color_temprature_slider_lora_weight: float = 0.0, seed: Optional[int] = None, mask_image: Optional[Union[MediaFile, str, bytes]] = None, tile_image: Optional[Union[MediaFile, str, bytes]] = None, img2img_image: Optional[Union[MediaFile, str, bytes]] = None, lineart_image: Optional[Union[MediaFile, str, bytes]] = None, scribble_image: Optional[Union[MediaFile, str, bytes]] = None, brightness_image: Optional[Union[MediaFile, str, bytes]] = None, inpainting_image: Optional[Union[MediaFile, str, bytes]] = None, ip_adapter_image: Optional[Union[MediaFile, str, bytes]] = None, negative_auto_mask_text: Optional[str] = None, positive_auto_mask_text: Optional[str] = None, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            prompt: Prompt - using compel, use +++ to increase words weight:: doc: https://github.com/damian0815/compel/tree/main/doc || https://invoke-ai.github.io/InvokeAI/features/PROMPTS/#attention-weighting
            
            eta: Controls the amount of noise that is added to the input data during the denoising diffusion process. Higher value -> more noise Defaults to 0.0.
            
            max_width: Max width/Resolution of image Defaults to 512.
            
            scheduler: Choose a scheduler. Defaults to 'DDIM'.
            
            guess_mode: In this mode, the ControlNet encoder will try best to recognize the content of the input image even if you remove all prompts. The `guidance_scale` between 3.0 and 5.0 is recommended. Defaults to False.
            
            int_kwargs: int_kwargs Defaults to ''.
            
            max_height: Max height/Resolution of image Defaults to 512.
            
            num_outputs: Number of images to generate Defaults to 1.
            
            guidance_scale: Scale for classifier-free guidance Defaults to 7.0.
            
            ip_adapter_ckpt: IP Adapter checkpoint Defaults to 'ip-adapter_sd15.bin'.
            
            negative_prompt: Negative prompt - using compel, use +++ to increase words weight//// negative-embeddings available ///// FastNegativeV2 , boring_e621_v4 , verybadimagenegative_v1 || to use them, write their keyword in negative prompt Defaults to 'Longbody, lowres, bad anatomy, bad hands, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality'.
            
            img2img_strength: img2img strength, does not work when inpainting image is given, 0.1-same image, 0.99-complete destruction of image Defaults to 0.5.
            
            ip_adapter_weight: IP Adapter weight Defaults to 1.0.
            
            sorted_controlnets: Comma seperated string of controlnet names, list of names: tile, inpainting, lineart,depth ,scribble , brightness /// example value: tile, inpainting, lineart  Defaults to 'lineart, tile, inpainting'.
            
            inpainting_strength: inpainting strength Defaults to 1.0.
            
            num_inference_steps: Steps to run denoising Defaults to 20.
            
            disable_safety_check: Disable safety check. Use at your own risk! Defaults to False.
            
            film_grain_lora_weight: disabled on 0 Defaults to 0.0.
            
            tile_conditioning_scale: Conditioning scale for tile controlnet Defaults to 1.0.
            
            add_more_detail_lora_scale: Scale/ weight of more_details lora, more scale = more details, disabled on 0 Defaults to 0.5.
            
            detail_tweaker_lora_weight: disabled on 0 Defaults to 0.0.
            
            lineart_conditioning_scale: Conditioning scale for canny controlnet Defaults to 1.0.
            
            scribble_conditioning_scale: Conditioning scale for scribble controlnet Defaults to 1.0.
            
            epi_noise_offset_lora_weight: disabled on 0 Defaults to 0.0.
            
            brightness_conditioning_scale: Conditioning scale for brightness controlnet Defaults to 1.0.
            
            inpainting_conditioning_scale: Conditioning scale for inpaint controlnet Defaults to 1.0.
            
            color_temprature_slider_lora_weight: disabled on 0 Defaults to 0.0.
            
            seed: Seed Optional.
            
            mask_image: mask image for inpainting controlnet Optional.
            
            tile_image: Control image for tile controlnet Optional.
            
            img2img_image: Image2image image Optional.
            
            lineart_image: Control image for canny controlnet Optional.
            
            scribble_image: Control image for scribble controlnet Optional.
            
            brightness_image: Control image for brightness controlnet Optional.
            
            inpainting_image: Control image for inpainting controlnet Optional.
            
            ip_adapter_image: IP Adapter image Optional.
            
            negative_auto_mask_text: // seperated list of objects you dont want to mask - 'hairs // eyes // cloth'  Optional.
            
            positive_auto_mask_text: // seperated list of objects for mask, AI will auto create mask of these objects, if mask text is given, mask image will not work - 'hairs // eyes // cloth' Optional.
            
        """
        return self.submit_job("/predictions", prompt=prompt, eta=eta, max_width=max_width, scheduler=scheduler, guess_mode=guess_mode, int_kwargs=int_kwargs, max_height=max_height, num_outputs=num_outputs, guidance_scale=guidance_scale, ip_adapter_ckpt=ip_adapter_ckpt, negative_prompt=negative_prompt, img2img_strength=img2img_strength, ip_adapter_weight=ip_adapter_weight, sorted_controlnets=sorted_controlnets, inpainting_strength=inpainting_strength, num_inference_steps=num_inference_steps, disable_safety_check=disable_safety_check, film_grain_lora_weight=film_grain_lora_weight, tile_conditioning_scale=tile_conditioning_scale, add_more_detail_lora_scale=add_more_detail_lora_scale, detail_tweaker_lora_weight=detail_tweaker_lora_weight, lineart_conditioning_scale=lineart_conditioning_scale, scribble_conditioning_scale=scribble_conditioning_scale, epi_noise_offset_lora_weight=epi_noise_offset_lora_weight, brightness_conditioning_scale=brightness_conditioning_scale, inpainting_conditioning_scale=inpainting_conditioning_scale, color_temprature_slider_lora_weight=color_temprature_slider_lora_weight, seed=seed, mask_image=mask_image, tile_image=tile_image, img2img_image=img2img_image, lineart_image=lineart_image, scribble_image=scribble_image, brightness_image=brightness_image, inpainting_image=inpainting_image, ip_adapter_image=ip_adapter_image, negative_auto_mask_text=negative_auto_mask_text, positive_auto_mask_text=positive_auto_mask_text, **kwargs)
     