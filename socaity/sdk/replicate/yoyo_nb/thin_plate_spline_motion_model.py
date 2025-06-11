from fastsdk.fastSDK import FastSDK
from typing import Union

from media_toolkit import MediaFile


class thin_plate_spline_motion_model(FastSDK):
    """
    Generated client for thin_plate_spline_motion_model
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="80f59366-8702-4bda-9184-b517cf12128e", api_key=api_key)
    
    def predict(self, source_image: Union[MediaFile, str, bytes], driving_video: Union[MediaFile, str, bytes], dataset_name: str = 'vox', **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            source_image: Input source image.
            
            driving_video: Choose a micromotion.
            
            dataset_name: Choose a dataset. Defaults to 'vox'.
            
        """
        return self.submit_job("/predict", source_image=source_image, driving_video=driving_video, dataset_name=dataset_name, **kwargs)
     