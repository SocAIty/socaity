from fastsdk.fastSDK import FastSDK

class stable_audio_open_1_0(FastSDK):
    """
    Generated client for stable_audio_open_1_0
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="f2c86360-7f36-4741-b140-4d2a6bc09ec1", api_key=api_key)
    
    def predict(self, prompt: str, seed: int = -1, steps: int = 100, cfg_scale: float = 6.0, sigma_max: int = 500, sigma_min: float = 0.03, batch_size: int = 1, sampler_type: str = 'dpmpp-3m-sde', seconds_start: int = 0, seconds_total: int = 8, negative_prompt: str = '', init_noise_level: float = 1.0, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            prompt: prompt
            
            seed: seed Defaults to -1.
            
            steps: steps Defaults to 100.
            
            cfg_scale: cfg_scale Defaults to 6.0.
            
            sigma_max: sigma_max Defaults to 500.
            
            sigma_min: sigma_min Defaults to 0.03.
            
            batch_size: batch_size Defaults to 1.
            
            sampler_type: sampler_type Defaults to 'dpmpp-3m-sde'.
            
            seconds_start: seconds_start Defaults to 0.
            
            seconds_total: seconds_total Defaults to 8.
            
            negative_prompt: negative_prompt Defaults to ''.
            
            init_noise_level: init_noise_level Defaults to 1.0.
            
        """
        return self.submit_job("/predict", prompt=prompt, seed=seed, steps=steps, cfg_scale=cfg_scale, sigma_max=sigma_max, sigma_min=sigma_min, batch_size=batch_size, sampler_type=sampler_type, seconds_start=seconds_start, seconds_total=seconds_total, negative_prompt=negative_prompt, init_noise_level=init_noise_level, **kwargs)
     