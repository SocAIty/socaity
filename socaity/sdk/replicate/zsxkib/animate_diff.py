from fastsdk import FastSDK, APISeex

class animate_diff(FastSDK):
    """
    Generated client for zsxkib/animate-diff
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="c5a85c36-0d23-47e1-b8d9-ab13ce68f709", api_key=api_key)
    
    def predictions(self, seed: int = -1, steps: int = 25, width: int = 512, frames: int = 16, height: int = 512, prompt: str = 'photo of vocano, rocks, storm weather, wind, lava waves, lightning, 8k uhd, dslr, soft lighting, high quality, film grain, Fujifilm XT3', base_model: str = 'realisticVisionV20_v20', output_format: str = 'mp4', guidance_scale: float = 7.5, negative_prompt: str = 'blur, haze, deformed iris, deformed pupils, semi-realistic, cgi, 3d, render, sketch, cartoon, drawing, anime, mutated hands and fingers, deformed, distorted, disfigured, poorly drawn, bad anatomy, wrong anatomy, extra limb, missing limb, floating limbs, disconnected limbs, mutation, mutated, ugly, disgusting, amputation', pan_up_motion_strength: float = 0.0, zoom_in_motion_strength: float = 0.0, pan_down_motion_strength: float = 0.0, pan_left_motion_strength: float = 0.0, zoom_out_motion_strength: float = 0.0, pan_right_motion_strength: float = 0.0, rolling_clockwise_motion_strength: float = 0.0, rolling_anticlockwise_motion_strength: float = 0.0, **kwargs) -> APISeex:
        """
        
        
        
        Args:
            seed: Seed for different images and reproducibility. Use -1 to randomise seed Defaults to -1.
            
            steps: Number of inference steps Defaults to 25.
            
            width: Width in pixels Defaults to 512.
            
            frames: Length of the video in frames (playback is at 8 fps e.g. 16 frames @ 8 fps is 2 seconds) Defaults to 16.
            
            height: Height in pixels Defaults to 512.
            
            prompt: prompt Defaults to 'photo of vocano, rocks, storm weather, wind, lava waves, lightning, 8k uhd, dslr, soft lighting, high quality, film grain, Fujifilm XT3'.
            
            base_model: Select a base model (DreamBooth checkpoint) Defaults to 'realisticVisionV20_v20'.
            
            output_format: Output format of the video. Can be 'mp4' or 'gif' Defaults to 'mp4'.
            
            guidance_scale: Guidance Scale. How closely do we want to adhere to the prompt and its contents Defaults to 7.5.
            
            negative_prompt: negative_prompt Defaults to 'blur, haze, deformed iris, deformed pupils, semi-realistic, cgi, 3d, render, sketch, cartoon, drawing, anime, mutated hands and fingers, deformed, distorted, disfigured, poorly drawn, bad anatomy, wrong anatomy, extra limb, missing limb, floating limbs, disconnected limbs, mutation, mutated, ugly, disgusting, amputation'.
            
            pan_up_motion_strength: Strength of Pan Up Motion LoRA. 0 disables the LoRA Defaults to 0.0.
            
            zoom_in_motion_strength: Strength of Zoom In Motion LoRA. 0 disables the LoRA Defaults to 0.0.
            
            pan_down_motion_strength: Strength of Pan Down Motion LoRA. 0 disables the LoRA Defaults to 0.0.
            
            pan_left_motion_strength: Strength of Pan Left Motion LoRA. 0 disables the LoRA Defaults to 0.0.
            
            zoom_out_motion_strength: Strength of Zoom Out Motion LoRA. 0 disables the LoRA Defaults to 0.0.
            
            pan_right_motion_strength: Strength of Pan Right Motion LoRA. 0 disables the LoRA Defaults to 0.0.
            
            rolling_clockwise_motion_strength: Strength of Rolling Clockwise Motion LoRA. 0 disables the LoRA Defaults to 0.0.
            
            rolling_anticlockwise_motion_strength: Strength of Rolling Anticlockwise Motion LoRA. 0 disables the LoRA Defaults to 0.0.
            
        """
        return self.submit_job("/predictions", seed=seed, steps=steps, width=width, frames=frames, height=height, prompt=prompt, base_model=base_model, output_format=output_format, guidance_scale=guidance_scale, negative_prompt=negative_prompt, pan_up_motion_strength=pan_up_motion_strength, zoom_in_motion_strength=zoom_in_motion_strength, pan_down_motion_strength=pan_down_motion_strength, pan_left_motion_strength=pan_left_motion_strength, zoom_out_motion_strength=zoom_out_motion_strength, pan_right_motion_strength=pan_right_motion_strength, rolling_clockwise_motion_strength=rolling_clockwise_motion_strength, rolling_anticlockwise_motion_strength=rolling_anticlockwise_motion_strength, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions