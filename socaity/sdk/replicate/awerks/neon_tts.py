from fastsdk.fastSDK import FastSDK

class neon_tts(FastSDK):
    """
    Generated client for neon_tts
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="58f5fbca-50c3-434a-b7d3-a9cbd55afbe1", api_key=api_key)
    
    def predict(self, text: str, language: str = 'en', **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            text: Input text for Text-to-Speech conversion
            
            language: Language of the text Defaults to 'en'.
            
        """
        return self.submit_job("/predict", text=text, language=language, **kwargs)
     