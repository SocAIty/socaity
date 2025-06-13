from fastsdk.fastSDK import FastSDK
from typing import Union

from media_toolkit import MediaFile


class deep3d(FastSDK):
    """
    Generated client for lucataco/deep3d
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="2a83dbc4-4a08-4d65-bc04-8192adf0324b", api_key=api_key)
    
    def predict(self, video: Union[MediaFile, str, bytes], model: str = 'deep3d_v1.0_640x360', **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            video: Input video
            
            model: Model size Defaults to 'deep3d_v1.0_640x360'.
            
        """
        return self.submit_job("/predictions", video=video, model=model, **kwargs)
     