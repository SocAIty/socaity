from fastsdk.fastSDK import FastSDK
from typing import Union, Optional

from media_toolkit import MediaFile


class florence_2_large(FastSDK):
    """
    Generated client for lucataco/florence-2-large
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="e45381de-1d62-4126-af47-130a1cbacc25", api_key=api_key)
    
    def predict(self, image: Union[MediaFile, str, bytes], task_input: str = 'Caption', text_input: Optional[str] = None, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            image: Grayscale input image
            
            task_input: Input task Defaults to 'Caption'.
            
            text_input: Text Input(Optional) Optional.
            
        """
        return self.submit_job("/predictions", image=image, task_input=task_input, text_input=text_input, **kwargs)
     