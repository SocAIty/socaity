from fastsdk.fastSDK import FastSDK

class pheme(FastSDK):
    """
    Generated client for pheme
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="454776dd-70c0-4b05-94cc-f357c613ab3d", api_key=api_key)
    
    def predict(self, top_k: int = 210, voice: str = 'male_voice', prompt: str = 'I gotta say, I would never expect that to happen!', temperature: float = 0.7, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            top_k: Top k Defaults to 210.
            
            voice: Voice to use Defaults to 'male_voice'.
            
            prompt: Input text Defaults to 'I gotta say, I would never expect that to happen!'.
            
            temperature: Temperature Defaults to 0.7.
            
        """
        return self.submit_job("/predict", top_k=top_k, voice=voice, prompt=prompt, temperature=temperature, **kwargs)
     