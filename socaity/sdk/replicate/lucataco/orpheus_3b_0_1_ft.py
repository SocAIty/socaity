from fastsdk.fastSDK import FastSDK

class orpheus_3b_0_1_ft(FastSDK):
    """
    Generated client for orpheus_3b_0_1_ft
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="f9eafebb-5070-4df8-8047-26a0ea18b967", api_key=api_key)
    
    def predict(self, text: str, top_p: float = 0.95, voice: str = 'tara', temperature: float = 0.6, max_new_tokens: int = 1200, repetition_penalty: float = 1.1, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            text: Text to convert to speech
            
            top_p: Top P for nucleus sampling Defaults to 0.95.
            
            voice: Voice to use Defaults to 'tara'.
            
            temperature: Temperature for generation Defaults to 0.6.
            
            max_new_tokens: Maximum number of tokens to generate Defaults to 1200.
            
            repetition_penalty: Repetition penalty Defaults to 1.1.
            
        """
        return self.submit_job("/predict", text=text, top_p=top_p, voice=voice, temperature=temperature, max_new_tokens=max_new_tokens, repetition_penalty=repetition_penalty, **kwargs)
     