from fastsdk import FastSDK, APISeex
from typing import Union

from media_toolkit import MediaFile


class robust_video_matting(FastSDK):
    """
    Generated client for arielreplicate/robust-video-matting
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="708b7613-02bb-4077-becf-ff55eb4f2fb2", api_key=api_key)
    
    def predictions(self, input_video: Union[MediaFile, str, bytes], output_type: str = 'green-screen', **kwargs) -> APISeex:
        """
        Run a single prediction on the model
        
        
        Args:
            input_video: Video to segment.
            
            output_type: output_type Defaults to 'green-screen'.
            
        """
        return self.submit_job("/predictions", input_video=input_video, output_type=output_type, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions