from fastsdk.fastSDK import FastSDK
from typing import Union

from media_toolkit import MediaFile


class spanish_f5_tts(FastSDK):
    """
    Generated client for spanish_f5_tts
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="3514cf90-8b33-4367-9db5-77fdf9d3b0f0", api_key=api_key)
    
    def predict(self, gen_text: str, ref_text: str, ref_audio: Union[MediaFile, str, bytes], remove_silence: bool = True, custom_split_words: str = '', **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            gen_text: Text to Generate
            
            ref_text: Reference Text
            
            ref_audio: Reference audio for voice cloning
            
            remove_silence: Automatically remove silences? Defaults to True.
            
            custom_split_words: Custom split words, comma separated Defaults to ''.
            
        """
        return self.submit_job("/predict", gen_text=gen_text, ref_text=ref_text, ref_audio=ref_audio, remove_silence=remove_silence, custom_split_words=custom_split_words, **kwargs)
     