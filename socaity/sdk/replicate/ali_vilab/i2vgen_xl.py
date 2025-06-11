from fastsdk.fastSDK import FastSDK
from typing import Optional, Union

from media_toolkit import MediaFile


class i2vgen_xl(FastSDK):
    """
    Generated client for i2vgen_xl
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="79e13ea6-d348-4bde-9b49-1de4d32890e2", api_key=api_key)
    
    def predict(self, image: Union[MediaFile, str, bytes], prompt: str, max_frames: int = 16, guidance_scale: float = 9.0, num_inference_steps: int = 50, seed: Optional[int] = None, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            image: Input image.
            
            prompt: Describe the input image.
            
            max_frames: Number of frames in the output Defaults to 16.
            
            guidance_scale: Scale for classifier-free guidance Defaults to 9.0.
            
            num_inference_steps: Number of denoising steps Defaults to 50.
            
            seed: Random seed. Leave blank to randomize the seed Optional.
            
        """
        return self.submit_job("/predict", image=image, prompt=prompt, max_frames=max_frames, guidance_scale=guidance_scale, num_inference_steps=num_inference_steps, seed=seed, **kwargs)
     