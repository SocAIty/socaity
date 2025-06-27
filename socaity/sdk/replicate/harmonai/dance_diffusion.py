from fastsdk import FastSDK, APISeex

class dance_diffusion(FastSDK):
    """
    Generated client for harmonai/dance-diffusion
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="63b878a3-2f74-4d25-9782-08e6254869dc", api_key=api_key)
    
    def predictions(self, steps: int = 100, length: float = 8.0, batch_size: int = 1, model_name: str = 'maestro-150k', **kwargs) -> APISeex:
        """
        
        
        
        Args:
            steps: Number of steps, higher numbers will give more refined output but will take longer. The maximum is 150. Defaults to 100.
            
            length: Number of seconds to generate Defaults to 8.0.
            
            batch_size: How many samples to generate Defaults to 1.
            
            model_name: Model Defaults to 'maestro-150k'.
            
        """
        return self.submit_job("/predictions", steps=steps, length=length, batch_size=batch_size, model_name=model_name, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions