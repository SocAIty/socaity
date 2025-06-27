from fastsdk import FastSDK, APISeex
from typing import Optional, Union

from media_toolkit import MediaFile


class jina_clip_v2(FastSDK):
    """
    Generated client for zsxkib/jina-clip-v2
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="2978d47d-bd47-41d1-8d9e-e77e35fc0153", api_key=api_key)
    
    def predictions(self, embedding_dim: int = 64, output_format: str = 'base64', text: Optional[str] = None, image: Optional[Union[str, MediaFile, bytes]] = None, **kwargs) -> APISeex:
        """
        
        
        
        Args:
            embedding_dim: Matryoshka dimension - output embedding dimension (64-1024) Defaults to 64.
            
            output_format: Format to use in outputs Defaults to 'base64'.
            
            text: Text content to embed (up to 8192 tokens). If both text and image provided, text embedding will be first in returned list. Optional.
            
            image: Image file to embed (optimal size: 512x512). If both text and image provided, image embedding will be second in returned list. Optional.
            
        """
        return self.submit_job("/predictions", embedding_dim=embedding_dim, output_format=output_format, text=text, image=image, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions