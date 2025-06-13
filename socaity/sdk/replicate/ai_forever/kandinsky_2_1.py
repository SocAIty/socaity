from fastsdk.fastSDK import FastSDK
from typing import Union, Optional

from media_toolkit import MediaFile


class kandinsky_2_1(FastSDK):
    """
    Generated client for ai-forever/kandinsky-2-1
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="89ca03f9-0f9c-4a7a-b45e-a3365b7e02a6", api_key=api_key)
    
    def predict(self, task: str = 'text2img', width: int = 512, height: int = 512, prompt: str = 'A alien cheeseburger creature eating itself, claymation, cinematic, moody lighting', strength: float = 0.3, num_outputs: int = 1, guidance_scale: float = 4.0, negative_prompt: str = 'low quality, bad quality', num_steps_prior: int = 25, num_inference_steps: int = 100, seed: Optional[int] = None, image: Optional[Union[MediaFile, str, bytes]] = None, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            task: Choose a task Defaults to 'text2img'.
            
            width: Width of output image. Reduce the seeting if hits memory limits Defaults to 512.
            
            height: Height of output image. Reduce the seeting if hits memory limits Defaults to 512.
            
            prompt: Provide input prompt Defaults to 'A alien cheeseburger creature eating itself, claymation, cinematic, moody lighting'.
            
            strength: indicates how much to transform the input iamge, valid for text_guided_img2img task. Defaults to 0.3.
            
            num_outputs: Number of images to output. Defaults to 1.
            
            guidance_scale: Scale for classifier-free guidance Defaults to 4.0.
            
            negative_prompt: Specify things to not see in the output for text2img and text_guided_img2img tasks Defaults to 'low quality, bad quality'.
            
            num_steps_prior: Number of denoising steps in prior Defaults to 25.
            
            num_inference_steps: Number of denoising steps Defaults to 100.
            
            seed: Random seed. Leave blank to randomize the seed Optional.
            
            image: Input image for text_guided_img2img task Optional.
            
        """
        return self.submit_job("/predictions", task=task, width=width, height=height, prompt=prompt, strength=strength, num_outputs=num_outputs, guidance_scale=guidance_scale, negative_prompt=negative_prompt, num_steps_prior=num_steps_prior, num_inference_steps=num_inference_steps, seed=seed, image=image, **kwargs)
     