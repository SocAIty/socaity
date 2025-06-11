from fastsdk.fastSDK import FastSDK
from typing import Union

from media_toolkit import MediaFile


class sam_2(FastSDK):
    """
    Generated client for sam_2
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="8782cde1-a5d3-4c91-b1be-8bd355b76151", api_key=api_key)
    
    def predict(self, image: Union[MediaFile, str, bytes], use_m2m: bool = True, points_per_side: int = 32, pred_iou_thresh: float = 0.88, stability_score_thresh: float = 0.95, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            image: Input image
            
            use_m2m: Use M2M Defaults to True.
            
            points_per_side: Points per side for mask generation Defaults to 32.
            
            pred_iou_thresh: Predicted IOU threshold Defaults to 0.88.
            
            stability_score_thresh: Stability score threshold Defaults to 0.95.
            
        """
        return self.submit_job("/predict", image=image, use_m2m=use_m2m, points_per_side=points_per_side, pred_iou_thresh=pred_iou_thresh, stability_score_thresh=stability_score_thresh, **kwargs)
     