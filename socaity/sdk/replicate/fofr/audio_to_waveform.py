from fastsdk.fastSDK import FastSDK
from typing import Union

from media_toolkit import MediaFile


class audio_to_waveform(FastSDK):
    """
    Generated client for fofr/audio-to-waveform
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="60f4f983-b431-4032-b387-28a93edb15e1", api_key=api_key)
    
    def predict(self, audio: Union[MediaFile, str, bytes], bg_color: str = '#000000', fg_alpha: float = 0.75, bar_count: int = 100, bar_width: float = 0.4, bars_color: str = '#ffffff', caption_text: str = '', **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            audio: Audio file to create waveform from
            
            bg_color: Background color of waveform Defaults to '#000000'.
            
            fg_alpha: Opacity of foreground waveform Defaults to 0.75.
            
            bar_count: Number of bars in waveform Defaults to 100.
            
            bar_width: Width of bars in waveform. 1 represents full width, 0.5 represents half width, etc. Defaults to 0.4.
            
            bars_color: Color of waveform bars Defaults to '#ffffff'.
            
            caption_text: Caption text for the video Defaults to ''.
            
        """
        return self.submit_job("/predictions", audio=audio, bg_color=bg_color, fg_alpha=fg_alpha, bar_count=bar_count, bar_width=bar_width, bars_color=bars_color, caption_text=caption_text, **kwargs)
     