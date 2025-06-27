from fastsdk import FastSDK, APISeex
from typing import Union

from media_toolkit import MediaFile


class gfpgan(FastSDK):
    """
    Generated client for tencentarc/gfpgan
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="41ba6470-a630-4bf4-9b9a-b76c7bc07484", api_key=api_key)
    
    def predictions(self, img: Union[str, MediaFile, bytes], scale: float = 2.0, version: str = 'v1.4', **kwargs) -> APISeex:
        """
        
        
        
        Args:
            img: Input
            
            scale: Rescaling factor Defaults to 2.0.
            
            version: GFPGAN version. v1.3: better quality. v1.4: more details and better identity. Defaults to 'v1.4'.
            
        """
        return self.submit_job("/predictions", img=img, scale=scale, version=version, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions