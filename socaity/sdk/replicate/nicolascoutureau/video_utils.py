from fastsdk import FastSDK, APISeex
from typing import Union

from media_toolkit import MediaFile


class video_utils(FastSDK):
    """
    Generated client for nicolascoutureau/video-utils
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="ff5b0116-92a4-490c-9d7c-6f64b1092882", api_key=api_key)
    
    def predictions(self, task: str, input_file: Union[str, MediaFile, bytes], fps: int = 0, **kwargs) -> APISeex:
        """
        
        
        
        Args:
            task: Task to perform
            
            input_file: File – zip, image or video to process
            
            fps: frames per second, if relevant. Use 0 to keep original fps (or use default). Converting to GIF defaults to 12fps Defaults to 0.
            
        """
        return self.submit_job("/predictions", task=task, input_file=input_file, fps=fps, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions