from fastsdk.fastSDK import FastSDK
from typing import Optional, Union

from media_toolkit import MediaFile


class florence_2_large(FastSDK):
    """
    Generated client for florence_2_large
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="4531d47b-bd90-4aa5-b2e5-ca26eefdd118", api_key=api_key)
    
    def predict(self, image: Union[MediaFile, str, bytes], task_input: str = 'Caption', text_input: Optional[str] = None, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            image: Grayscale input image
            
            task_input: Input task Defaults to 'Caption'.
            
            text_input: Text Input(Optional) Optional.
            
        """
        return self.submit_job("/predict", image=image, task_input=task_input, text_input=text_input, **kwargs)
     