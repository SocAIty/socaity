from fastsdk.fastSDK import FastSDK
from typing import Optional, Union

from media_toolkit import MediaFile


class edit_video_by_editing_text(FastSDK):
    """
    Generated client for edit_video_by_editing_text
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="f3205738-27ae-42b6-9d13-8e68a1d051b9", api_key=api_key)
    
    def predict(self, video_in: Union[MediaFile, str, bytes], mode: str = 'transcribe', split_at: str = 'word', transcription: Optional[str] = None, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            video_in: Video file to transcribe or edit
            
            mode: Mode: either transcribe or edit Defaults to 'transcribe'.
            
            split_at: When using mode 'edit', split transcription at the word level or character level. Default: word level. Character level is more precise but can lead to matching errors. Defaults to 'word'.
            
            transcription: When using mode 'edit', this should be the transcription of the desired output video. Use mode 'transcribe' to create a starting point. Optional.
            
        """
        return self.submit_job("/predict", video_in=video_in, mode=mode, split_at=split_at, transcription=transcription, **kwargs)
     