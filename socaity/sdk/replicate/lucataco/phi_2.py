from fastsdk import FastSDK, APISeex

class phi_2(FastSDK):
    """
    Generated client for lucataco/phi-2
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="ce54bb7f-20cf-46b6-94bd-b83766b62268", api_key=api_key)
    
    def predictions(self, prompt: str, max_length: int = 200, **kwargs) -> APISeex:
        """
        Run a single prediction on the model
        
        
        Args:
            prompt: Input prompt
            
            max_length: Max length Defaults to 200.
            
        """
        return self.submit_job("/predictions", prompt=prompt, max_length=max_length, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions