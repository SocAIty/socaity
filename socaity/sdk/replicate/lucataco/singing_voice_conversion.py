from fastsdk import FastSDK, APISeex
from typing import Union

from media_toolkit import MediaFile


class singing_voice_conversion(FastSDK):
    """
    Generated client for lucataco/singing-voice-conversion
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="03f4b34b-cd6d-425d-a9b3-6272ae4cb4df", api_key=api_key)
    
    def predictions(self, source_audio: Union[str, MediaFile, bytes], target_singer: str = 'Taylor Swift', key_shift_mode: int = 0, pitch_shift_control: str = 'Auto Shift', diffusion_inference_steps: int = 1000, **kwargs) -> APISeex:
        """
        
        
        
        Args:
            source_audio: Input source audio file
            
            target_singer: Target singer to convert audio to Defaults to 'Taylor Swift'.
            
            key_shift_mode: Key shift values Defaults to 0.
            
            pitch_shift_control: Pitch shift control Defaults to 'Auto Shift'.
            
            diffusion_inference_steps: Diffusion inference steps Defaults to 1000.
            
        """
        return self.submit_job("/predictions", source_audio=source_audio, target_singer=target_singer, key_shift_mode=key_shift_mode, pitch_shift_control=pitch_shift_control, diffusion_inference_steps=diffusion_inference_steps, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions