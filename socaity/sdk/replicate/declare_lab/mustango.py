from fastsdk import FastSDK, APISeex

class mustango(FastSDK):
    """
    Generated client for declare-lab/mustango
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="e0c02659-b190-490c-8839-0684746c3730", api_key=api_key)
    
    def predictions(self, steps: int = 100, prompt: str = "This is a new age piece. There is a flute playing the main melody with a lot of staccato notes. The rhythmic background consists of a medium tempo electronic drum beat with percussive elements all over the spectrum. There is a playful atmosphere to the piece. This piece can be used in the soundtrack of a children's TV show or an advertisement jingle.", guidance: float = 3.0, **kwargs) -> APISeex:
        """
        Run a single prediction on the model
        
        
        Args:
            steps: inference steps Defaults to 100.
            
            prompt: Input prompt. Defaults to "This is a new age piece. There is a flute playing the main melody with a lot of staccato notes. The rhythmic background consists of a medium tempo electronic drum beat with percussive elements all over the spectrum. There is a playful atmosphere to the piece. This piece can be used in the soundtrack of a children's TV show or an advertisement jingle.".
            
            guidance: guidance scale Defaults to 3.0.
            
        """
        return self.submit_job("/predictions", steps=steps, prompt=prompt, guidance=guidance, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions