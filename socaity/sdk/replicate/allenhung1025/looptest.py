from fastsdk.fastSDK import FastSDK

class looptest(FastSDK):
    """
    Generated client for looptest
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="512bc71c-85f1-46f3-bc60-799cc2c6cd77", api_key=api_key)
    
    def predict(self, seed: int = -1, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            seed: Set seed, -1 for random Defaults to -1.
            
        """
        return self.submit_job("/predict", seed=seed, **kwargs)
     