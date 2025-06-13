from fastsdk.fastSDK import FastSDK
from typing import Union

from media_toolkit import MediaFile


class mars5_tts(FastSDK):
    """
    Generated client for platform-kit/mars5-tts
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="ece24dd4-0ae3-4a1c-826b-b7467f1a2f91", api_key=api_key)
    
    def predict(self, text: str = "Hi there, I'm your new voice clone, powered by Mars5.", top_k: int = 95, temperature: float = 0.5, freq_penalty: int = 3, ref_audio_file: Union[MediaFile, str, bytes] = 'https://replicate.delivery/pbxt/L9a6SelzU0B2DIWeNpkNR0CKForWSbkswoUP69L0NLjLswVV/voice_sample.wav', rep_penalty_window: int = 95, ref_audio_transcript: str = "Hi there. I'm your new voice clone. Try your best to upload quality audio.", **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            text: Text to synthesize Defaults to "Hi there, I'm your new voice clone, powered by Mars5.".
            
            top_k: top_k Defaults to 95.
            
            temperature: temperature Defaults to 0.5.
            
            freq_penalty: freq_penalty Defaults to 3.
            
            ref_audio_file: Reference audio file to clone from <= 10 seconds Defaults to 'https://replicate.delivery/pbxt/L9a6SelzU0B2DIWeNpkNR0CKForWSbkswoUP69L0NLjLswVV/voice_sample.wav'.
            
            rep_penalty_window: rep_penalty_window Defaults to 95.
            
            ref_audio_transcript: Text in the reference audio file Defaults to "Hi there. I'm your new voice clone. Try your best to upload quality audio.".
            
        """
        return self.submit_job("/predictions", text=text, top_k=top_k, temperature=temperature, freq_penalty=freq_penalty, ref_audio_file=ref_audio_file, rep_penalty_window=rep_penalty_window, ref_audio_transcript=ref_audio_transcript, **kwargs)
     