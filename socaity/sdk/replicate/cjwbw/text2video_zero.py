from fastsdk.fastSDK import FastSDK
from typing import Optional


class text2video_zero(FastSDK):
    """
    Generated client for text2video_zero
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="1bb90cc5-bfbe-461a-8c4e-436ba13e1464", api_key=api_key)
    
    def predict(self, fps: int = 4, prompt: str = 'A horse galloping on a street', model_name: str = 'dreamlike-art/dreamlike-photoreal-2.0', timestep_t0: int = 44, timestep_t1: int = 47, video_length: int = 20, negative_prompt: str = '', motion_field_strength_x: int = 12, motion_field_strength_y: int = 12, seed: Optional[int] = None, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            fps: video frames per second Defaults to 4.
            
            prompt: Input Prompt Defaults to 'A horse galloping on a street'.
            
            model_name: choose your model, the model should be avaliable on HF Defaults to 'dreamlike-art/dreamlike-photoreal-2.0'.
            
            timestep_t0: Perform DDPM steps from t0 to t1. The larger the gap between t0 and t1, the more variance between the frames. Ensure t0 < t1 Defaults to 44.
            
            timestep_t1: Perform DDPM steps from t0 to t1. The larger the gap between t0 and t1, the more variance between the frames. Ensure t0 < t1 Defaults to 47.
            
            video_length: Video length in seconds Defaults to 20.
            
            negative_prompt: Negative Prompt Defaults to ''.
            
            motion_field_strength_x: motion_field_strength_x Defaults to 12.
            
            motion_field_strength_y: motion_field_strength_y Defaults to 12.
            
            seed: Random seed. Leave blank to randomize the seed Optional.
            
        """
        return self.submit_job("/predict", fps=fps, prompt=prompt, model_name=model_name, timestep_t0=timestep_t0, timestep_t1=timestep_t1, video_length=video_length, negative_prompt=negative_prompt, motion_field_strength_x=motion_field_strength_x, motion_field_strength_y=motion_field_strength_y, seed=seed, **kwargs)
     