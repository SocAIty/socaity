from fastsdk.fastSDK import FastSDK

class mustango(FastSDK):
    """
    Generated client for mustango
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="8128be82-4cb3-4753-9304-5134dda7b7bd", api_key=api_key)
    
    def predict(self, steps: int = 100, prompt: str = "This is a new age piece. There is a flute playing the main melody with a lot of staccato notes. The rhythmic background consists of a medium tempo electronic drum beat with percussive elements all over the spectrum. There is a playful atmosphere to the piece. This piece can be used in the soundtrack of a children's TV show or an advertisement jingle.", guidance: float = 3.0, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            steps: inference steps Defaults to 100.
            
            prompt: Input prompt. Defaults to "This is a new age piece. There is a flute playing the main melody with a lot of staccato notes. The rhythmic background consists of a medium tempo electronic drum beat with percussive elements all over the spectrum. There is a playful atmosphere to the piece. This piece can be used in the soundtrack of a children's TV show or an advertisement jingle.".
            
            guidance: guidance scale Defaults to 3.0.
            
        """
        return self.submit_job("/predict", steps=steps, prompt=prompt, guidance=guidance, **kwargs)
     