from fastsdk import FastSDK, APISeex
from typing import Union

from media_toolkit import MediaFile


class film_frame_interpolation_for_large_motion(FastSDK):
    """
    Generated client for zsxkib/film-frame-interpolation-for-large-motion
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="138d2e16-0804-4e2e-916b-ea0f9b732cea", api_key=api_key)
    
    def predictions(self, mp4: Union[str, MediaFile, bytes], num_interpolation_steps: int = 3, playback_frames_per_second: int = 24, **kwargs) -> APISeex:
        """
        
        
        
        Args:
            mp4: Provide an mp4 video file for frame interpolation.
            
            num_interpolation_steps: Number of steps to interpolate between animation frames Defaults to 3.
            
            playback_frames_per_second: Specify the playback speed in frames per second. Defaults to 24.
            
        """
        return self.submit_job("/predictions", mp4=mp4, num_interpolation_steps=num_interpolation_steps, playback_frames_per_second=playback_frames_per_second, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions