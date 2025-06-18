from fastsdk import FastSDK, APISeex

class nomic_embed_text_v1(FastSDK):
    """
    Generated client for lucataco/nomic-embed-text-v1
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="98467a14-427e-4efb-8ffb-4a10cc89a4fc", api_key=api_key)
    
    def predictions(self, sentences: str, **kwargs) -> APISeex:
        """
        Run a single prediction on the model
        
        
        Args:
            sentences: Input Sentence list - Each sentence should be split by a newline
            
        """
        return self.submit_job("/predictions", sentences=sentences, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions