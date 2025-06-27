from fastsdk import FastSDK, APISeex
from typing import Union

from media_toolkit import MediaFile


class autotune(FastSDK):
    """
    Generated client for nateraw/autotune
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="bb298a70-019d-4d23-b498-2888f630419f", api_key=api_key)
    
    def predictions(self, audio_file: Union[str, MediaFile, bytes], scale: str = 'closest', output_format: str = 'wav', **kwargs) -> APISeex:
        """
        
        
        
        Args:
            audio_file: Audio input file
            
            scale: Strategy for normalizing audio. Defaults to 'closest'.
            
            output_format: Output format for generated audio. Defaults to 'wav'.
            
        """
        return self.submit_job("/predictions", audio_file=audio_file, scale=scale, output_format=output_format, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions