from fastsdk.fastSDK import FastSDK

class emopia(FastSDK):
    """
    Generated client for annahung31/emopia
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="0c8acf67-d668-45ed-b08a-fafcdb97aa57", api_key=api_key)
    
    def predict(self, seed: int = -1, emotion: str = 'High valence, high arousal', **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            seed: Random seed, -1 for random Defaults to -1.
            
            emotion: Emotion to generate for Defaults to 'High valence, high arousal'.
            
        """
        return self.submit_job("/predictions", seed=seed, emotion=emotion, **kwargs)
     