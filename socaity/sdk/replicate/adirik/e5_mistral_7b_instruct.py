from fastsdk import FastSDK, APISeex
from typing import Optional


class e5_mistral_7b_instruct(FastSDK):
    """
    Generated client for adirik/e5-mistral-7b-instruct
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="f57685da-80aa-4e92-914a-c3e8faeae92d", api_key=api_key)
    
    def predictions(self, document: str, normalize: bool = False, task: Optional[str] = None, query: Optional[str] = None, **kwargs) -> APISeex:
        """
        Run a single prediction on the model
        
        
        Args:
            document: The document to be used.
            
            normalize: Whether to output the normalized embeddings or not. Defaults to False.
            
            task: The task description. Optional.
            
            query: The query to be used. Optional.
            
        """
        return self.submit_job("/predictions", document=document, normalize=normalize, task=task, query=query, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions