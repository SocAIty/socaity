from fastsdk import FastSDK, APISeex

class llama_2_13b_embeddings(FastSDK):
    """
    Generated client for andreasjansson/llama-2-13b-embeddings
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="760818eb-ff3f-4cfa-9c7c-1156dc83e0b1", api_key=api_key)
    
    def predictions(self, prompts: str, prompt_separator: str = '\n\n', **kwargs) -> APISeex:
        """
        
        
        
        Args:
            prompts: List of prompts, separated by prompt_separator. Maximum 100 prompts per prediction.
            
            prompt_separator: Separator between prompts Defaults to '\n\n'.
            
        """
        return self.submit_job("/predictions", prompts=prompts, prompt_separator=prompt_separator, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions