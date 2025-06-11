from fastsdk.fastSDK import FastSDK
from typing import Optional, Union

from media_toolkit import MediaFile


class illusion(FastSDK):
    """
    Generated client for illusion
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="93627c4e-174a-4f47-bcab-4477e0fa8707", api_key=api_key)
    
    def predict(self, prompt: str, qr_code_content: str, seed: int = -1, width: int = 768, border: int = 1, height: int = 768, num_outputs: int = 1, guidance_scale: float = 7.5, negative_prompt: str = 'ugly, disfigured, low quality, blurry, nsfw', qrcode_background: str = 'gray', num_inference_steps: int = 40, controlnet_conditioning_scale: float = 2.2, image: Optional[Union[MediaFile, str, bytes]] = None, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            prompt: The prompt to guide QR Code generation.
            
            qr_code_content: The website/content your QR Code will point to.
            
            seed: Seed Defaults to -1.
            
            width: Width out the output image Defaults to 768.
            
            border: QR code border size Defaults to 1.
            
            height: Height out the output image Defaults to 768.
            
            num_outputs: Number of outputs Defaults to 1.
            
            guidance_scale: Scale for classifier-free guidance Defaults to 7.5.
            
            negative_prompt: The negative prompt to guide image generation. Defaults to 'ugly, disfigured, low quality, blurry, nsfw'.
            
            qrcode_background: Background color of raw QR code Defaults to 'gray'.
            
            num_inference_steps: Number of diffusion steps Defaults to 40.
            
            controlnet_conditioning_scale: The outputs of the controlnet are multiplied by `controlnet_conditioning_scale` before they are added to the residual in the original unet. Defaults to 2.2.
            
            image: Input image. If none is provided, a QR code will be generated Optional.
            
        """
        return self.submit_job("/predict", prompt=prompt, qr_code_content=qr_code_content, seed=seed, width=width, border=border, height=height, num_outputs=num_outputs, guidance_scale=guidance_scale, negative_prompt=negative_prompt, qrcode_background=qrcode_background, num_inference_steps=num_inference_steps, controlnet_conditioning_scale=controlnet_conditioning_scale, image=image, **kwargs)
     