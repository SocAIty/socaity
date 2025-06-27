from fastsdk import FastSDK, APISeex

class orpheus_3b_0_1_ft(FastSDK):
    """
    Generated client for lucataco/orpheus-3b-0-1-ft
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="433abebd-7640-452f-827f-e17ab9c26264", api_key=api_key)
    
    def predictions(self, text: str, top_p: float = 0.95, voice: str = 'tara', temperature: float = 0.6, max_new_tokens: int = 1200, repetition_penalty: float = 1.1, **kwargs) -> APISeex:
        """
        
        
        
        Args:
            text: Text to convert to speech
            
            top_p: Top P for nucleus sampling Defaults to 0.95.
            
            voice: Voice to use Defaults to 'tara'.
            
            temperature: Temperature for generation Defaults to 0.6.
            
            max_new_tokens: Maximum number of tokens to generate Defaults to 1200.
            
            repetition_penalty: Repetition penalty Defaults to 1.1.
            
        """
        return self.submit_job("/predictions", text=text, top_p=top_p, voice=voice, temperature=temperature, max_new_tokens=max_new_tokens, repetition_penalty=repetition_penalty, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions