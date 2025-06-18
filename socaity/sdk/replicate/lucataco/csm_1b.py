from fastsdk import FastSDK, APISeex

class csm_1b(FastSDK):
    """
    Generated client for lucataco/csm-1b
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="a81aae22-ba41-4ed6-9a84-8cf99c8e3779", api_key=api_key)
    
    def predictions(self, text: str = 'Hello from Sesame.', speaker: int = 0, max_audio_length_ms: int = 10000, **kwargs) -> APISeex:
        """
        Run a single prediction on the model
        
        
        Args:
            text: Text to convert to speech Defaults to 'Hello from Sesame.'.
            
            speaker: Speaker ID (0 or 1) Defaults to 0.
            
            max_audio_length_ms: Maximum audio length in milliseconds Defaults to 10000.
            
        """
        return self.submit_job("/predictions", text=text, speaker=speaker, max_audio_length_ms=max_audio_length_ms, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions