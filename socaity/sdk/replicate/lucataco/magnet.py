from fastsdk import FastSDK, APISeex

class magnet(FastSDK):
    """
    Generated client for lucataco/magnet
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="e0de7ff2-1a9b-40ba-9c94-4c0f654d168d", api_key=api_key)
    
    def predictions(self, model: str = 'facebook/magnet-small-10secs', top_p: float = 0.9, prompt: str = '80s electronic track with melodic synthesizers, catchy beat and groovy bass', max_cfg: float = 10.0, min_cfg: float = 1.0, span_score: str = 'prod-stride1', variations: int = 3, temperature: float = 3.0, decoding_steps_stage_1: int = 20, decoding_steps_stage_2: int = 10, decoding_steps_stage_3: int = 10, decoding_steps_stage_4: int = 10, **kwargs) -> APISeex:
        """
        
        
        
        Args:
            model: Model to use Defaults to 'facebook/magnet-small-10secs'.
            
            top_p: Top p for sampling Defaults to 0.9.
            
            prompt: Input Text Defaults to '80s electronic track with melodic synthesizers, catchy beat and groovy bass'.
            
            max_cfg: Max CFG coefficient Defaults to 10.0.
            
            min_cfg: Min CFG coefficient Defaults to 1.0.
            
            span_score: span_score Defaults to 'prod-stride1'.
            
            variations: Number of variations to generate Defaults to 3.
            
            temperature: Temperature for sampling Defaults to 3.0.
            
            decoding_steps_stage_1: Number of decoding steps for stage 1 Defaults to 20.
            
            decoding_steps_stage_2: Number of decoding steps for stage 2 Defaults to 10.
            
            decoding_steps_stage_3: Number of decoding steps for stage 3 Defaults to 10.
            
            decoding_steps_stage_4: Number of decoding steps for stage 4 Defaults to 10.
            
        """
        return self.submit_job("/predictions", model=model, top_p=top_p, prompt=prompt, max_cfg=max_cfg, min_cfg=min_cfg, span_score=span_score, variations=variations, temperature=temperature, decoding_steps_stage_1=decoding_steps_stage_1, decoding_steps_stage_2=decoding_steps_stage_2, decoding_steps_stage_3=decoding_steps_stage_3, decoding_steps_stage_4=decoding_steps_stage_4, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions