from fastsdk.fastSDK import FastSDK

class dance_diffusion(FastSDK):
    """
    Generated client for dance_diffusion
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="edcbf0c6-f6a3-4ee6-9fcc-aab313b56bb5", api_key=api_key)
    
    def predict(self, steps: int = 100, length: float = 8.0, batch_size: int = 1, model_name: str = 'maestro-150k', **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            steps: Number of steps, higher numbers will give more refined output but will take longer. The maximum is 150. Defaults to 100.
            
            length: Number of seconds to generate Defaults to 8.0.
            
            batch_size: How many samples to generate Defaults to 1.
            
            model_name: Model Defaults to 'maestro-150k'.
            
        """
        return self.submit_job("/predict", steps=steps, length=length, batch_size=batch_size, model_name=model_name, **kwargs)
     