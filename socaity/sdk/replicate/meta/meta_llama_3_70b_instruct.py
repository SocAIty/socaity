from fastsdk.fastSDK import FastSDK

class meta_llama_3_70b_instruct(FastSDK):
    """
    Generated client for meta/meta-llama-3-70b-instruct
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="18956f9d-4f1c-42e3-9456-e44253ae19e2", api_key=api_key)
    
    def ready(self, **kwargs):
        """
        None
        
        """
        return self.submit_job("/ready", **kwargs)
    
    def predict(self, top_k: int = 50, top_p: float = 0.9, prompt: str = '', max_tokens: int = 512, min_tokens: int = 0, temperature: float = 0.6, prompt_template: str = '{prompt}', presence_penalty: float = 1.15, frequency_penalty: float = 0.2, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            top_k: The number of highest probability tokens to consider for generating the output. If > 0, only keep the top k tokens with highest probability (top-k filtering). Defaults to 50.
            
            top_p: A probability threshold for generating the output. If < 1.0, only keep the top tokens with cumulative probability >= top_p (nucleus filtering). Nucleus filtering is described in Holtzman et al. (http://arxiv.org/abs/1904.09751). Defaults to 0.9.
            
            prompt: Prompt Defaults to ''.
            
            max_tokens: The maximum number of tokens the model should generate as output. Defaults to 512.
            
            min_tokens: The minimum number of tokens the model should generate as output. Defaults to 0.
            
            temperature: The value used to modulate the next token probabilities. Defaults to 0.6.
            
            prompt_template: Prompt template. The string `{prompt}` will be substituted for the input prompt. If you want to generate dialog output, use this template as a starting point and construct the prompt string manually, leaving `prompt_template={prompt}`. Defaults to '{prompt}'.
            
            presence_penalty: Presence penalty Defaults to 1.15.
            
            frequency_penalty: Frequency penalty Defaults to 0.2.
            
        """
        return self.submit_job("/predictions", top_k=top_k, top_p=top_p, prompt=prompt, max_tokens=max_tokens, min_tokens=min_tokens, temperature=temperature, prompt_template=prompt_template, presence_penalty=presence_penalty, frequency_penalty=frequency_penalty, **kwargs)
     