from fastsdk.fastSDK import FastSDK

class stablelm_tuned_alpha_7b(FastSDK):
    """
    Generated client for stability-ai/stablelm-tuned-alpha-7b
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="c89dcbf6-be34-479b-8aa5-d5d6486bec1a", api_key=api_key)
    
    def predict(self, top_p: float = 1.0, prompt: str = "What's your mood today?", temperature: float = 0.75, max_new_tokens: int = 100, repetition_penalty: float = 1.2, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            top_p: Valid if you choose top_p decoding. When decoding text, samples from the top p percentage of most likely tokens; lower to ignore less likely tokens Defaults to 1.0.
            
            prompt: Input Prompt. Defaults to "What's your mood today?".
            
            temperature: Adjusts randomness of outputs, greater than 1 is random and 0 is deterministic, 0.75 is a good starting value. Defaults to 0.75.
            
            max_new_tokens: Maximum number of tokens to generate. A word is generally 2-3 tokens Defaults to 100.
            
            repetition_penalty: Penalty for repeated words in generated text; 1 is no penalty, values greater than 1 discourage repetition, less than 1 encourage it. Defaults to 1.2.
            
        """
        return self.submit_job("/predictions", top_p=top_p, prompt=prompt, temperature=temperature, max_new_tokens=max_new_tokens, repetition_penalty=repetition_penalty, **kwargs)
     