from fastsdk.fastSDK import FastSDK

class kokoro_82m(FastSDK):
    """
    Generated client for kokoro_82m
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="da504038-4412-41e4-ad1f-aa07bb8bf1e1", api_key=api_key)
    
    def predict(self, text: str, speed: float = 1.0, voice: str = 'af_bella', **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            text: Text input (long text is automatically split)
            
            speed: Speech speed multiplier (0.5 = half speed, 2.0 = double speed) Defaults to 1.0.
            
            voice: Voice to use for synthesis Defaults to 'af_bella'.
            
        """
        return self.submit_job("/predict", text=text, speed=speed, voice=voice, **kwargs)
     