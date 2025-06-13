from fastsdk.fastSDK import FastSDK
from typing import Optional


class qwen1_5_72b(FastSDK):
    """
    Generated client for lucataco/qwen1-5-72b
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="8cc9762d-a6ee-4062-8283-089ef558bc06", api_key=api_key)
    
    def predict(self, top_k: int = 1, top_p: float = 1.0, prompt: str = 'Give me a short introduction to large language model.', temperature: float = 1.0, system_prompt: str = 'You are a helpful assistant.', max_new_tokens: int = 512, repetition_penalty: float = 1.0, seed: Optional[int] = None, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            top_k: When decoding text, samples from the top k most likely tokens; lower to ignore less likely tokens. Defaults to 1.
            
            top_p: When decoding text, samples from the top p percentage of most likely tokens; lower to ignore less likely tokens. Defaults to 1.0.
            
            prompt: Input prompt Defaults to 'Give me a short introduction to large language model.'.
            
            temperature: Adjusts randomness of outputs, greater than 1 is random and 0 is deterministic, 0.75 is a good starting value. Defaults to 1.0.
            
            system_prompt: System prompt Defaults to 'You are a helpful assistant.'.
            
            max_new_tokens: The maximum number of tokens to generate Defaults to 512.
            
            repetition_penalty: Penalty for repeated words in generated text; 1 is no penalty, values greater than 1 discourage repetition, less than 1 encourage it. Defaults to 1.0.
            
            seed: The seed for the random number generator Optional.
            
        """
        return self.submit_job("/predictions", top_k=top_k, top_p=top_p, prompt=prompt, temperature=temperature, system_prompt=system_prompt, max_new_tokens=max_new_tokens, repetition_penalty=repetition_penalty, seed=seed, **kwargs)
     