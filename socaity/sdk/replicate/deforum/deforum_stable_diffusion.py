from fastsdk import FastSDK, APISeex
from typing import Optional


class deforum_stable_diffusion(FastSDK):
    """
    Generated client for deforum/deforum-stable-diffusion
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="2fd42d79-f34b-4c62-ac88-61c3ca7998b3", api_key=api_key)
    
    def predictions(self, fps: int = 15, zoom: str = '0: (1.04)', angle: str = '0:(0)', sampler: str = 'plms', max_frames: int = 100, translation_x: str = '0: (0)', translation_y: str = '0: (0)', color_coherence: str = 'Match Frame 0 LAB', animation_prompts: str = '0: a beautiful portrait of a woman by Artgerm, trending on Artstation', seed: Optional[int] = None, **kwargs) -> APISeex:
        """
        Run a single prediction on the model
        
        
        Args:
            fps: Choose fps for the video. Defaults to 15.
            
            zoom: zoom parameter for the motion Defaults to '0: (1.04)'.
            
            angle: angle parameter for the motion Defaults to '0:(0)'.
            
            sampler: sampler Defaults to 'plms'.
            
            max_frames: Number of frames for animation Defaults to 100.
            
            translation_x: translation_x parameter for the motion Defaults to '0: (0)'.
            
            translation_y: translation_y parameter for the motion Defaults to '0: (0)'.
            
            color_coherence: color_coherence Defaults to 'Match Frame 0 LAB'.
            
            animation_prompts: Prompt for animation. Provide 'frame number : prompt at this frame', separate different prompts with '|'. Make sure the frame number does not exceed the max_frames. Defaults to '0: a beautiful portrait of a woman by Artgerm, trending on Artstation'.
            
            seed: Random seed. Leave blank to randomize the seed Optional.
            
        """
        return self.submit_job("/predictions", fps=fps, zoom=zoom, angle=angle, sampler=sampler, max_frames=max_frames, translation_x=translation_x, translation_y=translation_y, color_coherence=color_coherence, animation_prompts=animation_prompts, seed=seed, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions