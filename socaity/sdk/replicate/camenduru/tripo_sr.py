from fastsdk.fastSDK import FastSDK
from typing import Union

from media_toolkit import MediaFile


class tripo_sr(FastSDK):
    """
    Generated client for tripo_sr
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="6eba2b75-f1eb-4003-a289-98d908d27ab1", api_key=api_key)
    
    def predict(self, image_path: Union[MediaFile, str, bytes], foreground_ratio: float = 0.85, do_remove_background: bool = True, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            image_path: Input Image
            
            foreground_ratio: foreground_ratio Defaults to 0.85.
            
            do_remove_background: do_remove_background Defaults to True.
            
        """
        return self.submit_job("/predict", image_path=image_path, foreground_ratio=foreground_ratio, do_remove_background=do_remove_background, **kwargs)
     