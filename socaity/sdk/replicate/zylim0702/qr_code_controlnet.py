from fastsdk import FastSDK, APISeex
from typing import Optional


class qr_code_controlnet(FastSDK):
    """
    Generated client for zylim0702/qr-code-controlnet
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="c0eedcb3-e8ef-4107-81b8-78c7e4e92e02", api_key=api_key)
    
    def predictions(self, url: str, prompt: str, eta: float = 0.0, scheduler: str = 'DDIM', guess_mode: bool = False, num_outputs: int = 1, guidance_scale: float = 9.0, negative_prompt: str = 'Longbody, lowres, bad anatomy, bad hands, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality', image_resolution: int = 768, num_inference_steps: int = 20, disable_safety_check: bool = False, qr_conditioning_scale: float = 1.0, seed: Optional[int] = None, **kwargs) -> APISeex:
        """
        Run a single prediction on the model
        
        
        Args:
            url: Link Url for QR Code.
            
            prompt: Prompt for the model
            
            eta: Controls the amount of noise that is added to the input data during the denoising diffusion process. Higher value -> more noise Defaults to 0.0.
            
            scheduler: Choose a scheduler. Defaults to 'DDIM'.
            
            guess_mode: In this mode, the ControlNet encoder will try best to recognize the content of the input image even if you remove all prompts. The `guidance_scale` between 3.0 and 5.0 is recommended. Defaults to False.
            
            num_outputs: Number of images to generate Defaults to 1.
            
            guidance_scale: Scale for classifier-free guidance Defaults to 9.0.
            
            negative_prompt: Negative prompt Defaults to 'Longbody, lowres, bad anatomy, bad hands, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality'.
            
            image_resolution: Resolution of image (smallest dimension) Defaults to 768.
            
            num_inference_steps: Steps to run denoising Defaults to 20.
            
            disable_safety_check: Disable safety check. Use at your own risk! Defaults to False.
            
            qr_conditioning_scale: Conditioning scale for qr controlnet Defaults to 1.0.
            
            seed: Seed Optional.
            
        """
        return self.submit_job("/predictions", url=url, prompt=prompt, eta=eta, scheduler=scheduler, guess_mode=guess_mode, num_outputs=num_outputs, guidance_scale=guidance_scale, negative_prompt=negative_prompt, image_resolution=image_resolution, num_inference_steps=num_inference_steps, disable_safety_check=disable_safety_check, qr_conditioning_scale=qr_conditioning_scale, seed=seed, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions