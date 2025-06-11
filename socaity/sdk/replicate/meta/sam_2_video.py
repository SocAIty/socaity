from fastsdk.fastSDK import FastSDK
from typing import Union

from media_toolkit import MediaFile


class sam_2_video(FastSDK):
    """
    Generated client for sam_2_video
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="48a12798-d215-49ad-b5df-37be2f1fae8f", api_key=api_key)
    
    def predict(self, input_video: Union[MediaFile, str, bytes], click_coordinates: str, mask_type: str = 'binary', video_fps: int = 30, click_frames: str = '0', click_labels: str = '1', output_video: bool = False, output_format: str = 'webp', output_quality: int = 80, annotation_type: str = 'mask', click_object_ids: str = '', output_frame_interval: int = 1, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            input_video: Input video file path
            
            click_coordinates: Click coordinates as '[x,y],[x,y],...'. Determines number of clicks.
            
            mask_type: Mask type: binary (B&W), highlighted (colored overlay), or greenscreen Defaults to 'binary'.
            
            video_fps: Video output frame rate (ignored for image sequence) Defaults to 30.
            
            click_frames: Frame indices for clicks as '0,0,150,0'. Auto-extends if shorter than coordinates. Defaults to '0'.
            
            click_labels: Click types (1=foreground, 0=background) as '1,1,0,1'. Auto-extends if shorter than coordinates. Defaults to '1'.
            
            output_video: True for video output, False for image sequence Defaults to False.
            
            output_format: Image format for sequence (ignored for video) Defaults to 'webp'.
            
            output_quality: JPG/WebP compression quality (0-100, ignored for PNG and video) Defaults to 80.
            
            annotation_type: Annotation type: mask only, bounding box only, or both (ignored for binary and greenscreen) Defaults to 'mask'.
            
            click_object_ids: Object labels for clicks as 'person,dog,cat'. Auto-generates if missing or incomplete. Defaults to ''.
            
            output_frame_interval: Output every Nth frame. 1=all frames, 2=every other, etc. Defaults to 1.
            
        """
        return self.submit_job("/predict", input_video=input_video, click_coordinates=click_coordinates, mask_type=mask_type, video_fps=video_fps, click_frames=click_frames, click_labels=click_labels, output_video=output_video, output_format=output_format, output_quality=output_quality, annotation_type=annotation_type, click_object_ids=click_object_ids, output_frame_interval=output_frame_interval, **kwargs)
     