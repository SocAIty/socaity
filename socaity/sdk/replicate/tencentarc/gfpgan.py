from fastsdk.fastSDK import FastSDK
from typing import Union

from media_toolkit import MediaFile


class gfpgan(FastSDK):
    """
    Generated client for gfpgan
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="8c831e4e-1f2c-4983-8e79-c68ab951bdc7", api_key=api_key)
    
    def predict(self, img: Union[MediaFile, str, bytes], scale: float = 2.0, version: str = 'v1.4', **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            img: Input
            
            scale: Rescaling factor Defaults to 2.0.
            
            version: GFPGAN version. v1.3: better quality. v1.4: more details and better identity. Defaults to 'v1.4'.
            
        """
        return self.submit_job("/predict", img=img, scale=scale, version=version, **kwargs)
     