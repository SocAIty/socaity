from fastsdk import FastSDK, APISeex

class embeddings_gte_base(FastSDK):
    """
    Generated client for mark3labs/embeddings-gte-base
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="6ebaf097-a13d-45fb-a4f6-43212da635cd", api_key=api_key)
    
    def predictions(self, text: str, **kwargs) -> APISeex:
        """
        Run a single prediction on the model
        
        
        Args:
            text: Text string to embed
            
        """
        return self.submit_job("/predictions", text=text, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions