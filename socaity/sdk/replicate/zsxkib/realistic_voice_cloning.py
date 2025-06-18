from fastsdk import FastSDK, APISeex
from typing import Optional, Union

from media_toolkit import MediaFile


class realistic_voice_cloning(FastSDK):
    """
    Generated client for zsxkib/realistic-voice-cloning
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="618b07ed-2cab-4ab9-9c79-ba83724ea423", api_key=api_key)
    
    def predictions(self, protect: float = 0.33, rvc_model: str = 'Squidward', index_rate: float = 0.5, reverb_size: float = 0.15, pitch_change: str = 'no-change', rms_mix_rate: float = 0.25, filter_radius: int = 3, output_format: str = 'mp3', reverb_damping: float = 0.7, reverb_dryness: float = 0.8, reverb_wetness: float = 0.2, crepe_hop_length: int = 128, pitch_change_all: float = 0.0, main_vocals_volume_change: float = 0.0, pitch_detection_algorithm: str = 'rmvpe', instrumental_volume_change: float = 0.0, backup_vocals_volume_change: float = 0.0, song_input: Optional[Union[MediaFile, str, bytes]] = None, custom_rvc_model_download_url: Optional[str] = None, **kwargs) -> APISeex:
        """
        Run a single prediction on the model
        
        
        Args:
            protect: Control how much of the original vocals' breath and voiceless consonants to leave in the AI vocals. Set 0.5 to disable. Defaults to 0.33.
            
            rvc_model: RVC model for a specific voice. If using a custom model, this should match the name of the downloaded model. If a 'custom_rvc_model_download_url' is provided, this will be automatically set to the name of the downloaded model. Defaults to 'Squidward'.
            
            index_rate: Control how much of the AI's accent to leave in the vocals. Defaults to 0.5.
            
            reverb_size: The larger the room, the longer the reverb time. Defaults to 0.15.
            
            pitch_change: Adjust pitch of AI vocals. Options: `no-change`, `male-to-female`, `female-to-male`. Defaults to 'no-change'.
            
            rms_mix_rate: Control how much to use the original vocal's loudness (0) or a fixed loudness (1). Defaults to 0.25.
            
            filter_radius: If >=3: apply median filtering median filtering to the harvested pitch results. Defaults to 3.
            
            output_format: wav for best quality and large file size, mp3 for decent quality and small file size. Defaults to 'mp3'.
            
            reverb_damping: Absorption of high frequencies in the reverb. Defaults to 0.7.
            
            reverb_dryness: Level of AI vocals without reverb. Defaults to 0.8.
            
            reverb_wetness: Level of AI vocals with reverb. Defaults to 0.2.
            
            crepe_hop_length: When `pitch_detection_algo` is set to `mangio-crepe`, this controls how often it checks for pitch changes in milliseconds. Lower values lead to longer conversions and higher risk of voice cracks, but better pitch accuracy. Defaults to 128.
            
            pitch_change_all: Change pitch/key of background music, backup vocals and AI vocals in semitones. Reduces sound quality slightly. Defaults to 0.0.
            
            main_vocals_volume_change: Control volume of main AI vocals. Use -3 to decrease the volume by 3 decibels, or 3 to increase the volume by 3 decibels. Defaults to 0.0.
            
            pitch_detection_algorithm: Best option is rmvpe (clarity in vocals), then mangio-crepe (smoother vocals). Defaults to 'rmvpe'.
            
            instrumental_volume_change: Control volume of the background music/instrumentals. Defaults to 0.0.
            
            backup_vocals_volume_change: Control volume of backup AI vocals. Defaults to 0.0.
            
            song_input: Upload your audio file here. Optional.
            
            custom_rvc_model_download_url: URL to download a custom RVC model. If provided, the model will be downloaded (if it doesn't already exist) and used for prediction, regardless of the 'rvc_model' value. Optional.
            
        """
        return self.submit_job("/predictions", protect=protect, rvc_model=rvc_model, index_rate=index_rate, reverb_size=reverb_size, pitch_change=pitch_change, rms_mix_rate=rms_mix_rate, filter_radius=filter_radius, output_format=output_format, reverb_damping=reverb_damping, reverb_dryness=reverb_dryness, reverb_wetness=reverb_wetness, crepe_hop_length=crepe_hop_length, pitch_change_all=pitch_change_all, main_vocals_volume_change=main_vocals_volume_change, pitch_detection_algorithm=pitch_detection_algorithm, instrumental_volume_change=instrumental_volume_change, backup_vocals_volume_change=backup_vocals_volume_change, song_input=song_input, custom_rvc_model_download_url=custom_rvc_model_download_url, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions