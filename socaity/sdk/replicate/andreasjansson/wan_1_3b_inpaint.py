from fastsdk.fastSDK import FastSDK
from typing import Union, Optional

from media_toolkit import MediaFile


class wan_1_3b_inpaint(FastSDK):
    """
    Generated client for wan_1_3b_inpaint
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="d29cac82-ac0f-423e-8e0c-01b016c8bb09", api_key=api_key)
    
    def predict(self, prompt: str, input_video: Union[MediaFile, str, bytes], seed: int = -1, strength: float = 0.9, expand_mask: int = 10, guide_scale: float = 5.0, sampling_steps: int = 50, negative_prompt: str = "", frames_per_second: int = 16, keep_aspect_ratio: bool = False, inpaint_fixup_steps: int = 0, mask_video: Optional[Union[MediaFile, str, bytes]] = None, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            prompt: Prompt for inpainting the masked area
            
            input_video: Original video to be inpainted
            
            seed: Random seed. Leave blank for random Defaults to -1.
            
            strength: Strength of inpainting effect, 1.0 is full regeneration Defaults to 0.9.
            
            expand_mask: Expand the mask by a number of pixels Defaults to 10.
            
            guide_scale: Guidance scale for prompt adherence Defaults to 5.0.
            
            sampling_steps: Number of sampling steps Defaults to 50.
            
            negative_prompt: Negative prompt Defaults to "".
            
            frames_per_second: Output video FPS Defaults to 16.
            
            keep_aspect_ratio: Keep the aspect ratio of the input video. This will degrade the quality of the inpainting. Defaults to False.
            
            inpaint_fixup_steps: Number of steps for final inpaint fixup. Ignored when in video-to-video mode (when mask_video is empty) Defaults to 0.
            
            mask_video: Mask video (white areas will be inpainted). Leave blank for video-to-video Optional.
            
        """
        return self.submit_job("/predict", prompt=prompt, input_video=input_video, seed=seed, strength=strength, expand_mask=expand_mask, guide_scale=guide_scale, sampling_steps=sampling_steps, negative_prompt=negative_prompt, frames_per_second=frames_per_second, keep_aspect_ratio=keep_aspect_ratio, inpaint_fixup_steps=inpaint_fixup_steps, mask_video=mask_video, **kwargs)
     