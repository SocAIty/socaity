from fastsdk.fastSDK import FastSDK

class audiogen(FastSDK):
    """
    Generated client for audiogen
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="6a13796a-1f9f-4910-bfbc-a1edebf9233b", api_key=api_key)
    
    def predict(self, prompt: str, top_k: int = 250, top_p: float = 0.0, duration: float = 3.0, temperature: float = 1.0, output_format: str = 'wav', classifier_free_guidance: int = 3, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            prompt: Prompt that describes the sound
            
            top_k: Reduces sampling to the k most likely tokens. Defaults to 250.
            
            top_p: Reduces sampling to tokens with cumulative probability of p. When set to  `0` (default), top_k sampling is used. Defaults to 0.0.
            
            duration: Max duration of the sound Defaults to 3.0.
            
            temperature: Controls the 'conservativeness' of the sampling process. Higher temperature means more diversity. Defaults to 1.0.
            
            output_format: Output format for generated audio. Defaults to 'wav'.
            
            classifier_free_guidance: Increases the influence of inputs on the output. Higher values produce lower-varience outputs that adhere more closely to inputs. Defaults to 3.
            
        """
        return self.submit_job("/predict", prompt=prompt, top_k=top_k, top_p=top_p, duration=duration, temperature=temperature, output_format=output_format, classifier_free_guidance=classifier_free_guidance, **kwargs)
     