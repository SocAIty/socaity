from fastsdk.fastSDK import FastSDK

class nomic_embed_text_v1(FastSDK):
    """
    Generated client for nomic_embed_text_v1
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="1821ed8d-6c7e-43f7-9dc0-8fbecf14bc5e", api_key=api_key)
    
    def predict(self, sentences: str, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            sentences: Input Sentence list - Each sentence should be split by a newline
            
        """
        return self.submit_job("/predict", sentences=sentences, **kwargs)
     