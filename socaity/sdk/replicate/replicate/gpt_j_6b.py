from fastsdk.fastSDK import FastSDK

class gpt_j_6b(FastSDK):
    """
    Generated client for gpt_j_6b
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="72874099-2722-4982-8cde-208fb6527ec2", api_key=api_key)
    
    def predict(self, prompt: str, top_k: int = 50, top_p: float = 1.0, decoding: str = 'top_p', max_length: int = 500, temperature: float = 0.75, repetition_penalty: float = 1.2, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            prompt: Input Prompt.
            
            top_k: Valid if you choose top_k decoding. The number of highest probability vocabulary tokens to keep for top-k-filtering Defaults to 50.
            
            top_p: Valid if you choose top_p decoding. When decoding text, samples from the top p percentage of most likely tokens; lower to ignore less likely tokens Defaults to 1.0.
            
            decoding: Choose a decoding method Defaults to 'top_p'.
            
            max_length: Maximum number of tokens to generate. A word is generally 2-3 tokens Defaults to 500.
            
            temperature: Adjusts randomness of outputs, greater than 1 is random and 0 is deterministic, 0.75 is a good starting value. Defaults to 0.75.
            
            repetition_penalty: Penalty for repeated words in generated text; 1 is no penalty, values greater than 1 discourage repetition, less than 1 encourage it. Defaults to 1.2.
            
        """
        return self.submit_job("/predict", prompt=prompt, top_k=top_k, top_p=top_p, decoding=decoding, max_length=max_length, temperature=temperature, repetition_penalty=repetition_penalty, **kwargs)
     