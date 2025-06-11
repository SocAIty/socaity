from fastsdk.fastSDK import FastSDK
from typing import Union

from media_toolkit import MediaFile


class hcflow_sr(FastSDK):
    """
    Generated client for hcflow_sr
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="1358e7ec-edad-4d06-82b5-e2a49ab88461", api_key=api_key)
    
    def predict(self, image: Union[MediaFile, str, bytes], model_type: str = 'celeb', **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            image: Low resolution image
            
            model_type: celeb photo or general image Defaults to 'celeb'.
            
        """
        return self.submit_job("/predict", image=image, model_type=model_type, **kwargs)
     