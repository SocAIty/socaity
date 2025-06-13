from fastsdk.fastSDK import FastSDK
from typing import Union, Optional

from media_toolkit import MediaFile


class bge_large_en_v1_5(FastSDK):
    """
    Generated client for nateraw/bge-large-en-v1-5
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="9a896975-5072-4e81-81b5-83756e6a5de1", api_key=api_key)
    
    def predict(self, texts: str = '', batch_size: int = 32, convert_to_numpy: bool = False, normalize_embeddings: bool = True, path: Optional[Union[MediaFile, str, bytes]] = None, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            texts: text to embed, formatted as JSON list of strings (e.g. ["hello", "world"]) Defaults to ''.
            
            batch_size: Batch size to use when processing text data. Defaults to 32.
            
            convert_to_numpy: When true, return output as npy file. By default, we return JSON Defaults to False.
            
            normalize_embeddings: Whether to normalize embeddings. Defaults to True.
            
            path: Path to file containing text as JSONL with 'text' field or valid JSON string list. Optional.
            
        """
        return self.submit_job("/predictions", texts=texts, batch_size=batch_size, convert_to_numpy=convert_to_numpy, normalize_embeddings=normalize_embeddings, path=path, **kwargs)
     