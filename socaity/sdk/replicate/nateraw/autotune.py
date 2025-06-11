from fastsdk.fastSDK import FastSDK
from typing import Union

from media_toolkit import MediaFile


class autotune(FastSDK):
    """
    Generated client for autotune
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="2ff453a1-9ace-4831-aaf5-99f91297ac67", api_key=api_key)
    
    def ready(self, **kwargs):
        """
        None
        
        """
        return self.submit_job("/ready", **kwargs)
    
    def predict(self, audio_file: Union[MediaFile, str, bytes], scale: str = 'closest', output_format: str = 'wav', **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            audio_file: Audio input file
            
            scale: Strategy for normalizing audio. Defaults to 'closest'.
            
            output_format: Output format for generated audio. Defaults to 'wav'.
            
        """
        return self.submit_job("/predict", audio_file=audio_file, scale=scale, output_format=output_format, **kwargs)
     