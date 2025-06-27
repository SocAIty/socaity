from fastsdk import FastSDK, APISeex
from typing import Optional, Union

from media_toolkit import MediaFile


class tortoise_tts(FastSDK):
    """
    Generated client for afiaka87/tortoise-tts
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="82a76d4e-73a1-4e7e-94d6-0e6f4b81519e", api_key=api_key)
    
    def predictions(self, seed: int = 0, text: str = 'The expressiveness of autoregressive transformers is literally nuts! I absolutely adore them.', preset: str = 'fast', voice_a: str = 'random', voice_b: str = 'disabled', voice_c: str = 'disabled', cvvp_amount: float = 0.0, custom_voice: Optional[Union[str, MediaFile, bytes]] = None, **kwargs) -> APISeex:
        """
        
        
        
        Args:
            seed: Random seed which can be used to reproduce results. Defaults to 0.
            
            text: Text to speak. Defaults to 'The expressiveness of autoregressive transformers is literally nuts! I absolutely adore them.'.
            
            preset: Which voice preset to use. See the documentation for more information. Defaults to 'fast'.
            
            voice_a: Selects the voice to use for generation. Use `random` to select a random voice. Use `custom_voice` to use a custom voice. Defaults to 'random'.
            
            voice_b: (Optional) Create new voice from averaging the latents for `voice_a`, `voice_b` and `voice_c`. Use `disabled` to disable voice mixing. Defaults to 'disabled'.
            
            voice_c: (Optional) Create new voice from averaging the latents for `voice_a`, `voice_b` and `voice_c`. Use `disabled` to disable voice mixing. Defaults to 'disabled'.
            
            cvvp_amount: How much the CVVP model should influence the output. Increasing this can in some cases reduce the likelyhood of multiple speakers. Defaults to 0 (disabled) Defaults to 0.0.
            
            custom_voice: (Optional) Create a custom voice based on an mp3 file of a speaker. Audio should be at least 15 seconds, only contain one speaker, and be in mp3 format. Overrides the `voice_a` input. Optional.
            
        """
        return self.submit_job("/predictions", seed=seed, text=text, preset=preset, voice_a=voice_a, voice_b=voice_b, voice_c=voice_c, cvvp_amount=cvvp_amount, custom_voice=custom_voice, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions