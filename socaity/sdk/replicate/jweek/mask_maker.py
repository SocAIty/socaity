from fastsdk.fastSDK import FastSDK
from typing import Union, Optional

from media_toolkit import MediaFile


class mask_maker(FastSDK):
    """
    Generated client for jweek/mask-maker
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="d1b3584b-c64d-4a9d-9a4a-539921f667e4", api_key=api_key)
    
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
        return self.submit_job("/predictions", image=image, threshold=threshold, mask_format=mask_format, mask_output=mask_output, mask_prompt=mask_prompt, **kwargs)
     