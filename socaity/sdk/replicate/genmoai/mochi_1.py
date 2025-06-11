from fastsdk.fastSDK import FastSDK
from typing import Optional


class mochi_1(FastSDK):
    """
    Generated client for mochi_1
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="3d2a4a38-c683-4ecb-833b-fcd1320ecba8", api_key=api_key)
    
    def predict(self, fps: int = 30, prompt: str = "Close-up of a chameleon's eye, with its scaly skin changing color. Ultra high resolution 4k.", num_frames: int = 163, guidance_scale: float = 6.0, num_inference_steps: int = 64, seed: Optional[int] = None, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            fps: Frames per second Defaults to 30.
            
            prompt: Focus on a single, central subject. Structure the prompt from coarse to fine details. Start with 'a close shot' or 'a medium shot' if applicable. Append 'high resolution 4k' to reduce warping Defaults to "Close-up of a chameleon's eye, with its scaly skin changing color. Ultra high resolution 4k.".
            
            num_frames: Number of frames to generate Defaults to 163.
            
            guidance_scale: The guidance scale for the model Defaults to 6.0.
            
            num_inference_steps: Number of inference steps Defaults to 64.
            
            seed: Random seed Optional.
            
        """
        return self.submit_job("/predict", fps=fps, prompt=prompt, num_frames=num_frames, guidance_scale=guidance_scale, num_inference_steps=num_inference_steps, seed=seed, **kwargs)
     