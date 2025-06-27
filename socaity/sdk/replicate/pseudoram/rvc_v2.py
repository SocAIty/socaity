from fastsdk import FastSDK, APISeex
from typing import Optional, Union

from media_toolkit import MediaFile


class rvc_v2(FastSDK):
    """
    Generated client for pseudoram/rvc-v2
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="ceaa8915-7b34-4775-b445-bf769fe8c5a2", api_key=api_key)
    
    def predictions(self, protect: float = 0.33, f0_method: str = 'rmvpe', rvc_model: str = 'Obama', index_rate: float = 0.5, pitch_change: float = 0.0, rms_mix_rate: float = 0.25, filter_radius: int = 3, output_format: str = 'mp3', crepe_hop_length: int = 128, input_audio: Optional[Union[str, MediaFile, bytes]] = None, custom_rvc_model_download_url: Optional[str] = None, **kwargs) -> APISeex:
        """
        
        
        
        Args:
            protect: Control how much of the original vocals' breath and voiceless consonants to leave in the AI vocals. Set 0.5 to disable. Defaults to 0.33.
            
            f0_method: Pitch detection algorithm. 'rmvpe' for clarity in vocals, 'mangio-crepe' for smoother vocals. Defaults to 'rmvpe'.
            
            rvc_model: RVC model for a specific voice. If using a custom model, this should match the name of the downloaded model. If a 'custom_rvc_model_download_url' is provided, this will be automatically set to the name of the downloaded model. Defaults to 'Obama'.
            
            index_rate: Control how much of the AI's accent to leave in the vocals. Defaults to 0.5.
            
            pitch_change: Adjust pitch of AI vocals in semitones. Use positive values to increase pitch, negative to decrease. Defaults to 0.0.
            
            rms_mix_rate: Control how much to use the original vocal's loudness (0) or a fixed loudness (1). Defaults to 0.25.
            
            filter_radius: If >=3: apply median filtering to the harvested pitch results. Defaults to 3.
            
            output_format: wav for best quality and large file size, mp3 for decent quality and small file size. Defaults to 'mp3'.
            
            crepe_hop_length: When `f0_method` is set to `mangio-crepe`, this controls how often it checks for pitch changes in milliseconds. Defaults to 128.
            
            input_audio: Upload your audio file here. Optional.
            
            custom_rvc_model_download_url: URL to download a custom RVC model. If provided, the model will be downloaded (if it doesn't already exist) and used for prediction, regardless of the 'rvc_model' value. Optional.
            
        """
        return self.submit_job("/predictions", protect=protect, f0_method=f0_method, rvc_model=rvc_model, index_rate=index_rate, pitch_change=pitch_change, rms_mix_rate=rms_mix_rate, filter_radius=filter_radius, output_format=output_format, crepe_hop_length=crepe_hop_length, input_audio=input_audio, custom_rvc_model_download_url=custom_rvc_model_download_url, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions