from fastsdk.fastSDK import FastSDK

class musicgen_looper(FastSDK):
    """
    Generated client for andreasjansson/musicgen-looper
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="2b08b99c-be1b-4904-85a9-3e4fcc9dda0e", api_key=api_key)
    
    def predict(self, prompt: str, bpm: float = 140.0, seed: int = -1, top_k: int = 250, top_p: float = 0.0, variations: int = 4, temperature: float = 1.0, max_duration: int = 8, model_version: str = 'medium', output_format: str = 'wav', classifier_free_guidance: int = 3, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            prompt: A description of the music you want to generate.
            
            bpm: Tempo in beats per minute Defaults to 140.0.
            
            seed: Seed for random number generator. If None or -1, a random seed will be used. Defaults to -1.
            
            top_k: Reduces sampling to the k most likely tokens. Defaults to 250.
            
            top_p: Reduces sampling to tokens with cumulative probability of p. When set to  `0` (default), top_k sampling is used. Defaults to 0.0.
            
            variations: Number of variations to generate Defaults to 4.
            
            temperature: Controls the 'conservativeness' of the sampling process. Higher temperature means more diversity. Defaults to 1.0.
            
            max_duration: Maximum duration of the generated loop in seconds. Defaults to 8.
            
            model_version: Model to use for generation. . Defaults to 'medium'.
            
            output_format: Output format for generated audio. Defaults to 'wav'.
            
            classifier_free_guidance: Increases the influence of inputs on the output. Higher values produce lower-varience outputs that adhere more closely to inputs. Defaults to 3.
            
        """
        return self.submit_job("/predictions", prompt=prompt, bpm=bpm, seed=seed, top_k=top_k, top_p=top_p, variations=variations, temperature=temperature, max_duration=max_duration, model_version=model_version, output_format=output_format, classifier_free_guidance=classifier_free_guidance, **kwargs)
     