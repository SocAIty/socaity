from fastsdk.fastSDK import FastSDK
from typing import Optional, Union

from media_toolkit import MediaFile


class tune_a_video(FastSDK):
    """
    Generated client for tune_a_video
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="fcf11e11-ef24-48c9-8fb2-d81e5fd8455f", api_key=api_key)
    
    def predict(self, steps: int = 300, width: int = 512, height: int = 512, length: int = 5, source_prompt: str = 'a man surfing', target_prompts: str = 'a panda surfing\na cartoon sloth surfing', sample_frame_rate: int = 1, video: Optional[Union[MediaFile, str, bytes]] = None, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            steps: number of steps to train for Defaults to 300.
            
            width: width of the output video (multiples of 32) Defaults to 512.
            
            height: height of the output video (multiples of 32) Defaults to 512.
            
            length: length of the output video (in seconds) Defaults to 5.
            
            source_prompt: prompts describing the original video Defaults to 'a man surfing'.
            
            target_prompts: prompts to change the video to Defaults to 'a panda surfing\na cartoon sloth surfing'.
            
            sample_frame_rate: with which rate to sample the input video Defaults to 1.
            
            video: input video Optional.
            
        """
        return self.submit_job("/predict", steps=steps, width=width, height=height, length=length, source_prompt=source_prompt, target_prompts=target_prompts, sample_frame_rate=sample_frame_rate, video=video, **kwargs)
     