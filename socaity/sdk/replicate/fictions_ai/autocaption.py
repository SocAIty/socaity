from fastsdk.fastSDK import FastSDK
from typing import Optional, Union

from media_toolkit import MediaFile


class autocaption(FastSDK):
    """
    Generated client for autocaption
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="ced0523c-daa5-4bd2-bd77-b9c764f957a0", api_key=api_key)
    
    def predict(self, video_file_input: Union[MediaFile, str, bytes], font: str = 'Poppins/Poppins-ExtraBold.ttf', color: str = 'white', kerning: float = -5.0, opacity: float = 0.0, ax_hars: int = 20, fontsize: float = 7.0, translate: bool = False, output_video: bool = True, stroke_color: str = 'black', stroke_width: float = 2.6, right_to_left: bool = False, subs_position: str = 'bottom75', highlight_color: str = 'yellow', output_transcript: bool = True, transcript_file_input: Optional[Union[MediaFile, str, bytes]] = None, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            video_file_input: Video file
            
            font: Font Defaults to 'Poppins/Poppins-ExtraBold.ttf'.
            
            color: Caption color Defaults to 'white'.
            
            kerning: Kerning for the subtitles Defaults to -5.0.
            
            opacity: Opacity for the subtitles background Defaults to 0.0.
            
            ax_hars: Max characters space for subtitles. 20 is good for videos, 10 is good for reels Defaults to 20.
            
            fontsize: Font size. 7.0 is good for videos, 4.0 is good for reels Defaults to 7.0.
            
            translate: Translate the subtitles to English Defaults to False.
            
            output_video: Output video, if true will output the video with subtitles Defaults to True.
            
            stroke_color: Stroke color Defaults to 'black'.
            
            stroke_width: Stroke width Defaults to 2.6.
            
            right_to_left: Right to left subtitles, for right to left languages. Only Arial fonts are supported. Defaults to False.
            
            subs_position: Subtitles position Defaults to 'bottom75'.
            
            highlight_color: Highlight color Defaults to 'yellow'.
            
            output_transcript: Output transcript json, if true will output a transcript file that you can edit and use for the next run in transcript_file_input Defaults to True.
            
            transcript_file_input: Transcript file, if provided will use this for words rather than whisper. Optional.
            
        """
        return self.submit_job("/predict", video_file_input=video_file_input, font=font, color=color, kerning=kerning, opacity=opacity, ax_hars=ax_hars, fontsize=fontsize, translate=translate, output_video=output_video, stroke_color=stroke_color, stroke_width=stroke_width, right_to_left=right_to_left, subs_position=subs_position, highlight_color=highlight_color, output_transcript=output_transcript, transcript_file_input=transcript_file_input, **kwargs)
     