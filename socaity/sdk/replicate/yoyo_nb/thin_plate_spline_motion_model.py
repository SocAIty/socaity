from fastsdk.fastSDK import FastSDK
from typing import Union

from media_toolkit import MediaFile


class thin_plate_spline_motion_model(FastSDK):
    """
    Generated client for yoyo-nb/thin-plate-spline-motion-model
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="d7f06376-5b6b-448d-b383-2081ba59c1c9", api_key=api_key)
    
    def predict(self, source_image: Union[MediaFile, str, bytes], driving_video: Union[MediaFile, str, bytes], dataset_name: str = 'vox', **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            source_image: Input source image.
            
            driving_video: Choose a micromotion.
            
            dataset_name: Choose a dataset. Defaults to 'vox'.
            
        """
        return self.submit_job("/predictions", source_image=source_image, driving_video=driving_video, dataset_name=dataset_name, **kwargs)
     