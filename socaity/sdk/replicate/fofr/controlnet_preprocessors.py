from fastsdk import FastSDK, APISeex
from typing import Union

from media_toolkit import MediaFile


class controlnet_preprocessors(FastSDK):
    """
    Generated client for fofr/controlnet-preprocessors
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="09029b7d-3fcc-42b6-b142-6839f9745612", api_key=api_key)
    
    def predictions(self, image: Union[MediaFile, str, bytes], hed: bool = True, sam: bool = True, mlsd: bool = True, pidi: bool = True, canny: bool = True, leres: bool = True, midas: bool = True, content: bool = True, lineart: bool = True, open_pose: bool = True, normal_bae: bool = True, face_detector: bool = True, lineart_anime: bool = True, **kwargs) -> APISeex:
        """
        Run a single prediction on the model
        
        
        Args:
            image: Image to preprocess
            
            hed: Run HED detection Defaults to True.
            
            sam: Run Sam detection Defaults to True.
            
            mlsd: Run MLSD detection Defaults to True.
            
            pidi: Run PidiNet detection Defaults to True.
            
            canny: Run canny edge detection Defaults to True.
            
            leres: Run Leres detection Defaults to True.
            
            midas: Run Midas detection Defaults to True.
            
            content: Run content shuffle detection Defaults to True.
            
            lineart: Run Lineart detection Defaults to True.
            
            open_pose: Run Openpose detection Defaults to True.
            
            normal_bae: Run NormalBae detection Defaults to True.
            
            face_detector: Run face detection Defaults to True.
            
            lineart_anime: Run LineartAnime detection Defaults to True.
            
        """
        return self.submit_job("/predictions", image=image, hed=hed, sam=sam, mlsd=mlsd, pidi=pidi, canny=canny, leres=leres, midas=midas, content=content, lineart=lineart, open_pose=open_pose, normal_bae=normal_bae, face_detector=face_detector, lineart_anime=lineart_anime, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions