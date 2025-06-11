from fastsdk.fastSDK import FastSDK
from typing import Union

from media_toolkit import MediaFile


class deep3d(FastSDK):
    """
    Generated client for deep3d
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="431f1496-5a7d-4854-be91-614eb35a7f66", api_key=api_key)
    
    def predict(self, video: Union[MediaFile, str, bytes], model: str = 'deep3d_v1.0_640x360', **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            video: Input video
            
            model: Model size Defaults to 'deep3d_v1.0_640x360'.
            
        """
        return self.submit_job("/predict", video=video, model=model, **kwargs)
     