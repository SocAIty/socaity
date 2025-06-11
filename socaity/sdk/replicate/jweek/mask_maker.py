from fastsdk.fastSDK import FastSDK
from typing import Optional, Union

from media_toolkit import MediaFile


class mask_maker(FastSDK):
    """
    Generated client for mask_maker
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="12233df1-2b13-4e12-a44b-3bd0038928f7", api_key=api_key)
    
    def predict(self, image: Union[MediaFile, str, bytes], threshold: float = 0.2, mask_format: str = 'coco_rle', mask_output: str = '', mask_prompt: Optional[str] = None, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            image: Input image file path or URL
            
            threshold: Confidence level for object detection Defaults to 0.2.
            
            mask_format: RLE encoding format for masks. 'coco_rle' (default) or 'custom_rle' Defaults to 'coco_rle'.
            
            mask_output: Single-line DSL defining composite masks (overrides default one-per-term).  Infix operators (left-to-right):    `&` → AND,  `|` or `+` → OR,  `A - B` → A AND NOT(B),  `-term` → NOT(term),  `XOR`.  Example: 'rider: man + horse; dog: dog' Defaults to ''.
            
            mask_prompt: Comma-separated names of the objects to be detected Optional.
            
        """
        return self.submit_job("/predict", image=image, threshold=threshold, mask_format=mask_format, mask_output=mask_output, mask_prompt=mask_prompt, **kwargs)
     