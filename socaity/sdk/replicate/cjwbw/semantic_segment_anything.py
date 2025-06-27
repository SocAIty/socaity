from fastsdk import FastSDK, APISeex
from typing import Union

from media_toolkit import MediaFile


class semantic_segment_anything(FastSDK):
    """
    Generated client for cjwbw/semantic-segment-anything
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="04c66564-04a1-43c6-85e1-5ce7a90f4339", api_key=api_key)
    
    def predictions(self, image: Union[str, MediaFile, bytes], output_json: bool = True, **kwargs) -> APISeex:
        """
        
        
        
        Args:
            image: Input image
            
            output_json: return raw json output Defaults to True.
            
        """
        return self.submit_job("/predictions", image=image, output_json=output_json, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions