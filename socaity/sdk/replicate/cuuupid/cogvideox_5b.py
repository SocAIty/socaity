from fastsdk.fastSDK import FastSDK

class cogvideox_5b(FastSDK):
    """
    Generated client for cuuupid/cogvideox-5b
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="579d6489-362b-4a37-b0fd-9ef14b7c8882", api_key=api_key)
    
    def ready(self, **kwargs):
        """
        None
        
        """
        return self.submit_job("/ready", **kwargs)
    
    def predict(self, prompt: str, seed: int = 42, steps: int = 50, guidance: float = 6.0, num_outputs: int = 1, extend_prompt: bool = True, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            prompt: Prompt
            
            seed: Seed for reproducibility. Defaults to 42.
            
            steps: # of inference steps, more steps can improve quality. Defaults to 50.
            
            guidance: The scale for classifier-free guidance, higher guidance can improve adherence to your prompt. Defaults to 6.0.
            
            num_outputs: # of output videos Defaults to 1.
            
            extend_prompt: If enabled, will use GLM-4 to make the prompt long (as intended for CogVideoX). Defaults to True.
            
        """
        return self.submit_job("/predictions", prompt=prompt, seed=seed, steps=steps, guidance=guidance, num_outputs=num_outputs, extend_prompt=extend_prompt, **kwargs)
     