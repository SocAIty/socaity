from fastsdk import FastSDK, APISeex
from typing import Optional


class sana(FastSDK):
    """
    Generated client for nvidia/sana
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="392df87f-336a-4d25-b0a1-ab03dec6a36a", api_key=api_key)
    
    def predictions(self, width: int = 1024, height: int = 1024, prompt: str = 'a cyberpunk cat with a neon sign that says "Sana"', model_variant: str = '1600M-1024px', guidance_scale: float = 5.0, negative_prompt: str = '', pag_guidance_scale: float = 2.0, num_inference_steps: int = 18, seed: Optional[int] = None, **kwargs) -> APISeex:
        """
        
        
        
        Args:
            width: Width of output image Defaults to 1024.
            
            height: Height of output image Defaults to 1024.
            
            prompt: Input prompt Defaults to 'a cyberpunk cat with a neon sign that says "Sana"'.
            
            model_variant: Model variant. 1600M variants are slower but produce higher quality than 600M, 1024px variants are optimized for 1024x1024px images, 512px variants are optimized for 512x512px images, 'multilang' variants can be prompted in both English and Chinese Defaults to '1600M-1024px'.
            
            guidance_scale: Classifier-free guidance scale Defaults to 5.0.
            
            negative_prompt: Specify things to not see in the output Defaults to ''.
            
            pag_guidance_scale: PAG Guidance scale Defaults to 2.0.
            
            num_inference_steps: Number of denoising steps Defaults to 18.
            
            seed: Random seed. Leave blank to randomize the seed Optional.
            
        """
        return self.submit_job("/predictions", width=width, height=height, prompt=prompt, model_variant=model_variant, guidance_scale=guidance_scale, negative_prompt=negative_prompt, pag_guidance_scale=pag_guidance_scale, num_inference_steps=num_inference_steps, seed=seed, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions