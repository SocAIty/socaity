from fastsdk import FastSDK, APISeex
from typing import Union

from media_toolkit import MediaFile


class tripo_sr(FastSDK):
    """
    Generated client for camenduru/tripo-sr
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="b776d683-2130-46a2-bd09-ef909b81bc0b", api_key=api_key)
    
    def predictions(self, image_path: Union[str, MediaFile, bytes], foreground_ratio: float = 0.85, do_remove_background: bool = True, **kwargs) -> APISeex:
        """
        
        
        
        Args:
            image_path: Input Image
            
            foreground_ratio: foreground_ratio Defaults to 0.85.
            
            do_remove_background: do_remove_background Defaults to True.
            
        """
        return self.submit_job("/predictions", image_path=image_path, foreground_ratio=foreground_ratio, do_remove_background=do_remove_background, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions