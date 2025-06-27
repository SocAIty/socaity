from fastsdk import FastSDK, APISeex
from typing import Optional, Union

from media_toolkit import MediaFile


class blip_2(FastSDK):
    """
    Generated client for andreasjansson/blip-2
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="184bb954-b6c9-4543-81f0-c455411aaad5", api_key=api_key)
    
    def predictions(self, image: Union[str, MediaFile, bytes], caption: bool = False, question: str = 'What is this a picture of?', temperature: float = 1.0, use_nucleus_sampling: bool = False, context: Optional[str] = None, **kwargs) -> APISeex:
        """
        
        
        
        Args:
            image: Input image to query or caption
            
            caption: Select if you want to generate image captions instead of asking questions Defaults to False.
            
            question: Question to ask about this image. Leave blank for captioning Defaults to 'What is this a picture of?'.
            
            temperature: Temperature for use with nucleus sampling Defaults to 1.0.
            
            use_nucleus_sampling: Toggles the model using nucleus sampling to generate responses Defaults to False.
            
            context: Optional - previous questions and answers to be used as context for answering current question Optional.
            
        """
        return self.submit_job("/predictions", image=image, caption=caption, question=question, temperature=temperature, use_nucleus_sampling=use_nucleus_sampling, context=context, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions