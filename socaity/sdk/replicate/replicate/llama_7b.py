from fastsdk.fastSDK import FastSDK

class llama_7b(FastSDK):
    """
    Generated client for replicate/llama-7b
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="dd6af761-d6b9-4a08-990d-2869397a679c", api_key=api_key)
    
    def predict(self, prompt: str, top_p: float = 0.95, max_gen_len: int = 256, temperature: float = 0.8, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            prompt: Text to prefix with 'hello '
            
            top_p: Top p value Defaults to 0.95.
            
            max_gen_len: Max generation length Defaults to 256.
            
            temperature: Temperature Defaults to 0.8.
            
        """
        return self.submit_job("/predictions", prompt=prompt, top_p=top_p, max_gen_len=max_gen_len, temperature=temperature, **kwargs)
     