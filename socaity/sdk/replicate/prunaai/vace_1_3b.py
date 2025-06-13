from fastsdk.fastSDK import FastSDK
from typing import Union, List, Optional, Any

from media_toolkit import MediaFile


class vace_1_3b(FastSDK):
    """
    Generated client for prunaai/vace-1-3b
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="44d72183-8b42-4bd5-92fb-faafd583a07e", api_key=api_key)
    
    def predict(self, prompt: str, seed: int = -1, size: str = '480*832', frame_num: int = 81, speed_mode: str = 'Lightly Juiced 🍊 (more consistent)', sample_shift: int = 16, sample_steps: int = 50, sample_solver: str = 'unipc', sample_guide_scale: float = 5.0, src_mask: Optional[Union[MediaFile, str, bytes]] = None, src_video: Optional[Union[MediaFile, str, bytes]] = None, src_ref_images: Optional[Union[List[Any], MediaFile, str, bytes]] = None, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            prompt: Prompt
            
            seed: Random seed (-1 for random) Defaults to -1.
            
            size: Output resolution Defaults to '480*832'.
            
            frame_num: Number of frames to generate. Defaults to 81.
            
            speed_mode: Speed optimization level Defaults to 'Lightly Juiced 🍊 (more consistent)'.
            
            sample_shift: Sample shift Defaults to 16.
            
            sample_steps: Sample steps Defaults to 50.
            
            sample_solver: Sample solver Defaults to 'unipc'.
            
            sample_guide_scale: Sample guide scale Defaults to 5.0.
            
            src_mask: Input mask video to edit. Optional.
            
            src_video: Input video to edit. Optional.
            
            src_ref_images: Input reference images to edit. Optional.
            
        """
        return self.submit_job("/predictions", prompt=prompt, seed=seed, size=size, frame_num=frame_num, speed_mode=speed_mode, sample_shift=sample_shift, sample_steps=sample_steps, sample_solver=sample_solver, sample_guide_scale=sample_guide_scale, src_mask=src_mask, src_video=src_video, src_ref_images=src_ref_images, **kwargs)
     