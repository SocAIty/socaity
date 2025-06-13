from fastsdk.fastSDK import FastSDK

class looptest(FastSDK):
    """
    Generated client for allenhung1025/looptest
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="2389def2-9430-486d-afbd-2cdd0631d659", api_key=api_key)
    
    def predict(self, seed: int = -1, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            seed: Set seed, -1 for random Defaults to -1.
            
        """
        return self.submit_job("/predictions", seed=seed, **kwargs)
     