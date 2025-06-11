from fastsdk.fastSDK import FastSDK

class phi_2(FastSDK):
    """
    Generated client for phi_2
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="af9b77b6-4890-48b8-86a7-b380c93f91f5", api_key=api_key)
    
    def predict(self, prompt: str, max_length: int = 200, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            prompt: Input prompt
            
            max_length: Max length Defaults to 200.
            
        """
        return self.submit_job("/predict", prompt=prompt, max_length=max_length, **kwargs)
     