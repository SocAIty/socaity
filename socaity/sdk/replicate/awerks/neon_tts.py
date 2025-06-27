from fastsdk import FastSDK, APISeex

class neon_tts(FastSDK):
    """
    Generated client for awerks/neon-tts
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="402dbd40-c083-44ca-b892-db9c53a2b54e", api_key=api_key)
    
    def predictions(self, text: str, language: str = 'en', **kwargs) -> APISeex:
        """
        
        
        
        Args:
            text: Input text for Text-to-Speech conversion
            
            language: Language of the text Defaults to 'en'.
            
        """
        return self.submit_job("/predictions", text=text, language=language, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions