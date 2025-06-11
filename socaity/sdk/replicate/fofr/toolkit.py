from fastsdk.fastSDK import FastSDK
from typing import Union

from media_toolkit import MediaFile


class toolkit(FastSDK):
    """
    Generated client for toolkit
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="7a54d069-0043-459a-ab7d-7654afe99013", api_key=api_key)
    
    def predict(self, task: str, input_file: Union[MediaFile, str, bytes], fps: int = 0, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            task: Task to perform
            
            input_file: File – zip, image or video to process
            
            fps: frames per second, if relevant. Use 0 to keep original fps (or use default). Converting to GIF defaults to 12fps Defaults to 0.
            
        """
        return self.submit_job("/predict", task=task, input_file=input_file, fps=fps, **kwargs)
     