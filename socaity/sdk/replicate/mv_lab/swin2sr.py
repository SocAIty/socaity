from fastsdk.fastSDK import FastSDK
from typing import Union

from media_toolkit import MediaFile


class swin2sr(FastSDK):
    """
    Generated client for swin2sr
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="46b8214e-73ab-41e9-b7e8-161f6244ed2b", api_key=api_key)
    
    def predict(self, image: Union[MediaFile, str, bytes], task: str = 'real_sr', **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            image: Input image
            
            task: Choose a task Defaults to 'real_sr'.
            
        """
        return self.submit_job("/predict", image=image, task=task, **kwargs)
     