from fastsdk.fastSDK import FastSDK
from typing import Optional


class e5_mistral_7b_instruct(FastSDK):
    """
    Generated client for e5_mistral_7b_instruct
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="84b839e4-7ab0-4331-8fc3-a697b317b3ce", api_key=api_key)
    
    def predict(self, document: str, normalize: bool = False, task: Optional[str] = None, query: Optional[str] = None, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            document: The document to be used.
            
            normalize: Whether to output the normalized embeddings or not. Defaults to False.
            
            task: The task description. Optional.
            
            query: The query to be used. Optional.
            
        """
        return self.submit_job("/predict", document=document, normalize=normalize, task=task, query=query, **kwargs)
     