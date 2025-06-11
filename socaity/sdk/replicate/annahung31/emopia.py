from fastsdk.fastSDK import FastSDK

class emopia(FastSDK):
    """
    Generated client for emopia
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="ad807e9b-d573-4cf6-9393-0b45014d409c", api_key=api_key)
    
    def predict(self, seed: int = -1, emotion: str = 'High valence, high arousal', **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            seed: Random seed, -1 for random Defaults to -1.
            
            emotion: Emotion to generate for Defaults to 'High valence, high arousal'.
            
        """
        return self.submit_job("/predict", seed=seed, emotion=emotion, **kwargs)
     