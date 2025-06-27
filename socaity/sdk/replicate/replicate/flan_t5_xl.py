from fastsdk import FastSDK, APISeex

class flan_t5_xl(FastSDK):
    """
    Generated client for replicate/flan-t5-xl
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="505dcfd9-4852-4a03-a1d5-7dbbc4367f90", api_key=api_key)
    
    def predictions(self, prompt: str, debug: bool = False, top_p: float = 1.0, max_length: int = 50, temperature: float = 0.75, repetition_penalty: float = 1.0, **kwargs) -> APISeex:
        """
        
        
        
        Args:
            prompt: Prompt to send to FLAN-T5.
            
            debug: provide debugging output in logs Defaults to False.
            
            top_p: When decoding text, samples from the top p percentage of most likely tokens; lower to ignore less likely tokens Defaults to 1.0.
            
            max_length: Maximum number of tokens to generate. A word is generally 2-3 tokens Defaults to 50.
            
            temperature: Adjusts randomness of outputs, greater than 1 is random and 0 is deterministic, 0.75 is a good starting value. Defaults to 0.75.
            
            repetition_penalty: Penalty for repeated words in generated text; 1 is no penalty, values greater than 1 discourage repetition, less than 1 encourage it. Defaults to 1.0.
            
        """
        return self.submit_job("/predictions", prompt=prompt, debug=debug, top_p=top_p, max_length=max_length, temperature=temperature, repetition_penalty=repetition_penalty, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions