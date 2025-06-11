from fastsdk.fastSDK import FastSDK

class yi_6b(FastSDK):
    """
    Generated client for yi_6b
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="f34601b5-9ba9-428d-90fc-6327e35d1793", api_key=api_key)
    
    def predict(self, prompt: str, top_k: int = 50, top_p: float = 0.95, temperature: float = 0.8, max_new_tokens: int = 512, prompt_template: str = '{prompt}', presence_penalty: float = 0.0, frequency_penalty: float = 0.0, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            prompt: prompt
            
            top_k: The number of highest probability tokens to consider for generating the output. If > 0, only keep the top k tokens with highest probability (top-k filtering). Defaults to 50.
            
            top_p: A probability threshold for generating the output. If < 1.0, only keep the top tokens with cumulative probability >= top_p (nucleus filtering). Nucleus filtering is described in Holtzman et al. (http://arxiv.org/abs/1904.09751). Defaults to 0.95.
            
            temperature: The value used to modulate the next token probabilities. Defaults to 0.8.
            
            max_new_tokens: The maximum number of tokens the model should generate as output. Defaults to 512.
            
            prompt_template: The template used to format the prompt. The input prompt is inserted into the template using the `{prompt}` placeholder. Defaults to '{prompt}'.
            
            presence_penalty: Presence penalty Defaults to 0.0.
            
            frequency_penalty: Frequency penalty Defaults to 0.0.
            
        """
        return self.submit_job("/predict", prompt=prompt, top_k=top_k, top_p=top_p, temperature=temperature, max_new_tokens=max_new_tokens, prompt_template=prompt_template, presence_penalty=presence_penalty, frequency_penalty=frequency_penalty, **kwargs)
     