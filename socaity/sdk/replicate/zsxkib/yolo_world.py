from fastsdk.fastSDK import FastSDK
from typing import Union

from media_toolkit import MediaFile


class yolo_world(FastSDK):
    """
    Generated client for zsxkib/yolo-world
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="41a54615-ab8a-4af0-ac7e-19c1d5378234", api_key=api_key)
    
    def predict(self, input_media: Union[MediaFile, str, bytes], nms_thr: float = 0.5, score_thr: float = 0.05, class_names: str = 'dog, eye, tongue, ear, leash, backpack, person, nose', max_num_boxes: int = 100, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            input_media: Path to the input image or video
            
            nms_thr: NMS threshold Defaults to 0.5.
            
            score_thr: Score threshold for displaying bounding boxes Defaults to 0.05.
            
            class_names: Enter the classes to be detected, separated by comma Defaults to 'dog, eye, tongue, ear, leash, backpack, person, nose'.
            
            max_num_boxes: Maximum number of bounding boxes to display Defaults to 100.
            
        """
        return self.submit_job("/predictions", input_media=input_media, nms_thr=nms_thr, score_thr=score_thr, class_names=class_names, max_num_boxes=max_num_boxes, **kwargs)
     