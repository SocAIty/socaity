from fastsdk.fastSDK import FastSDK

class embeddings_gte_base(FastSDK):
    """
    Generated client for embeddings_gte_base
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="789c6af5-6802-4644-9f0e-9c18048a6c85", api_key=api_key)
    
    def predict(self, text: str, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            text: Text string to embed
            
        """
        return self.submit_job("/predict", text=text, **kwargs)
     