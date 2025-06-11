from fastsdk.fastSDK import FastSDK
from typing import Union

from media_toolkit import MediaFile


class semantic_segment_anything(FastSDK):
    """
    Generated client for semantic_segment_anything
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="2be7f65b-ae84-44c6-b1cc-c9aaeebe9ec1", api_key=api_key)
    
    def predict(self, image: Union[MediaFile, str, bytes], output_json: bool = True, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            image: Input image
            
            output_json: return raw json output Defaults to True.
            
        """
        return self.submit_job("/predict", image=image, output_json=output_json, **kwargs)
     