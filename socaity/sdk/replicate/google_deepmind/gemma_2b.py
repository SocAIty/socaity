from fastsdk.fastSDK import FastSDK

class gemma_2b(FastSDK):
    """
    Generated client for gemma_2b
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="5fd18a2d-82e6-43e5-8603-8ff0c4bf31ac", api_key=api_key)
    
    def predict(self, top_k: int = 50, top_p: float = 0.95, prompt: str = 'Write me a poem about Machine Learning.', temperature: float = 0.7, max_new_tokens: int = 200, min_new_tokens: int = -1, repetition_penalty: float = 1.0, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            top_k: When decoding text, samples from the top k most likely tokens; lower to ignore less likely tokens Defaults to 50.
            
            top_p: When decoding text, samples from the top p percentage of most likely tokens; lower to ignore less likely tokens Defaults to 0.95.
            
            prompt: Prompt to send to the model. Defaults to 'Write me a poem about Machine Learning.'.
            
            temperature: Adjusts randomness of outputs, greater than 1 is random and 0 is deterministic, 0.75 is a good starting value. Defaults to 0.7.
            
            max_new_tokens: Maximum number of tokens to generate. A word is generally 2-3 tokens Defaults to 200.
            
            min_new_tokens: Minimum number of tokens to generate. To disable, set to -1. A word is generally 2-3 tokens. Defaults to -1.
            
            repetition_penalty: A parameter that controls how repetitive text can be. Lower means more repetitive, while higher means less repetitive. Set to 1.0 to disable. Defaults to 1.0.
            
        """
        return self.submit_job("/predict", top_k=top_k, top_p=top_p, prompt=prompt, temperature=temperature, max_new_tokens=max_new_tokens, min_new_tokens=min_new_tokens, repetition_penalty=repetition_penalty, **kwargs)
     