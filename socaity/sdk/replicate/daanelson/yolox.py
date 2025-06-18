from fastsdk import FastSDK, APISeex
from typing import Union

from media_toolkit import MediaFile


class yolox(FastSDK):
    """
    Generated client for daanelson/yolox
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="cd41e5da-0dd9-4893-872a-df2692fc91aa", api_key=api_key)
    
    def predictions(self, input_image: Union[MediaFile, str, bytes], nms: float = 0.3, conf: float = 0.3, tsize: int = 640, model_name: str = 'yolox-s', return_json: bool = False, **kwargs) -> APISeex:
        """
        Run a single prediction on the model
        
        
        Args:
            input_image: Path to an image
            
            nms: NMS threshold: NMS removes redundant detections. Detections with overlap percentage (IOU) above this threshold are consider redundant to each other and only one of them will be kept Defaults to 0.3.
            
            conf: Confidence threshold: Only detections with confidence higher are kept Defaults to 0.3.
            
            tsize: Resize image to this size Defaults to 640.
            
            model_name: Model name Defaults to 'yolox-s'.
            
            return_json: Return results in json format Defaults to False.
            
        """
        return self.submit_job("/predictions", input_image=input_image, nms=nms, conf=conf, tsize=tsize, model_name=model_name, return_json=return_json, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions