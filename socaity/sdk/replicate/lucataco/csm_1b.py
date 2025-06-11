from fastsdk.fastSDK import FastSDK

class csm_1b(FastSDK):
    """
    Generated client for csm_1b
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="0956874c-92c5-40fe-ad4f-f3e5e83451d6", api_key=api_key)
    
    def predict(self, text: str = 'Hello from Sesame.', speaker: int = 0, max_audio_length_ms: int = 10000, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            text: Text to convert to speech Defaults to 'Hello from Sesame.'.
            
            speaker: Speaker ID (0 or 1) Defaults to 0.
            
            max_audio_length_ms: Maximum audio length in milliseconds Defaults to 10000.
            
        """
        return self.submit_job("/predict", text=text, speaker=speaker, max_audio_length_ms=max_audio_length_ms, **kwargs)
     