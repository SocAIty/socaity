from fastsdk import FastSDK, APISeex

class audiogen(FastSDK):
    """
    Generated client for sepal/audiogen
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="736b4266-8a63-49a8-a405-7d94c1a8444b", api_key=api_key)
    
    def predictions(self, prompt: str, top_k: int = 250, top_p: float = 0.0, duration: float = 3.0, temperature: float = 1.0, output_format: str = 'wav', classifier_free_guidance: int = 3, **kwargs) -> APISeex:
        """
        
        
        
        Args:
            prompt: Prompt that describes the sound
            
            top_k: Reduces sampling to the k most likely tokens. Defaults to 250.
            
            top_p: Reduces sampling to tokens with cumulative probability of p. When set to  `0` (default), top_k sampling is used. Defaults to 0.0.
            
            duration: Max duration of the sound Defaults to 3.0.
            
            temperature: Controls the 'conservativeness' of the sampling process. Higher temperature means more diversity. Defaults to 1.0.
            
            output_format: Output format for generated audio. Defaults to 'wav'.
            
            classifier_free_guidance: Increases the influence of inputs on the output. Higher values produce lower-varience outputs that adhere more closely to inputs. Defaults to 3.
            
        """
        return self.submit_job("/predictions", prompt=prompt, top_k=top_k, top_p=top_p, duration=duration, temperature=temperature, output_format=output_format, classifier_free_guidance=classifier_free_guidance, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions