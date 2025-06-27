from fastsdk import FastSDK, APISeex
from typing import Optional, Union

from media_toolkit import MediaFile


class controlnet_1_1_x_realistic_vision_v2_0(FastSDK):
    """
    Generated client for usamaehsan/controlnet-1-1-x-realistic-vision-v2-0
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="0db6a1a4-eef9-44e2-b340-de3d3e96123d", api_key=api_key)
    
    def predictions(self, image: Union[str, MediaFile, bytes], steps: int = 20, prompt: str = '(a tabby cat)+++, high resolution, sitting on a park bench', strength: float = 0.8, max_width: float = 612.0, max_height: float = 612.0, guidance_scale: int = 10, negative_prompt: str = '(deformed iris, deformed pupils, semi-realistic, cgi, 3d, render, sketch, cartoon, drawing, anime:1.4), text, close up, cropped, out of frame, worst quality, low quality, jpeg artifacts, ugly, duplicate, morbid, mutilated, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, mutation, deformed, blurry, dehydrated, bad anatomy, bad proportions, extra limbs, cloned face, disfigured, gross proportions, malformed limbs, missing arms, missing legs, extra arms, extra legs, fused fingers, too many fingers, long neck', seed: Optional[int] = None, **kwargs) -> APISeex:
        """
        
        
        
        Args:
            image: Input image
            
            steps:  num_inference_steps Defaults to 20.
            
            prompt: prompt Defaults to '(a tabby cat)+++, high resolution, sitting on a park bench'.
            
            strength: control strength/weight Defaults to 0.8.
            
            max_width: max width of mask/image Defaults to 612.0.
            
            max_height: max height of mask/image Defaults to 612.0.
            
            guidance_scale: guidance_scale Defaults to 10.
            
            negative_prompt: negative_prompt Defaults to '(deformed iris, deformed pupils, semi-realistic, cgi, 3d, render, sketch, cartoon, drawing, anime:1.4), text, close up, cropped, out of frame, worst quality, low quality, jpeg artifacts, ugly, duplicate, morbid, mutilated, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, mutation, deformed, blurry, dehydrated, bad anatomy, bad proportions, extra limbs, cloned face, disfigured, gross proportions, malformed limbs, missing arms, missing legs, extra arms, extra legs, fused fingers, too many fingers, long neck'.
            
            seed: Leave blank to randomize Optional.
            
        """
        return self.submit_job("/predictions", image=image, steps=steps, prompt=prompt, strength=strength, max_width=max_width, max_height=max_height, guidance_scale=guidance_scale, negative_prompt=negative_prompt, seed=seed, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions