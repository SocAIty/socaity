from fastsdk import FastClient, APISeex
from typing import Optional, Literal

from media_toolkit import MediaFile


class chatterbox_multilingual(FastClient):
    """
    Generated client based on resemble-ai/chatterbox-multilingual format
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="0e0e491d-b412-4332-9ba6-790ae6e62a8a", api_key=api_key)
    
    def predictions(self, text: str, seed: int = 0, language: Literal["ar", "da", "de", "el", "en", "es", "fi", "fr", "he", "hi", "it", "ja", "ko", "ms", "nl", "no", "pl", "pt", "ru", "sv", "sw", "tr", "zh"] = 'en', cfg_weight: float = 0.5, temperature: float = 0.8, exaggeration: float = 0.5, reference_audio: Optional[MediaFile] = None, **kwargs) -> APISeex:
        """
        
        
        
        Args:
            text: Text to synthesize into speech (maximum 300 characters)
            
            seed: Random seed for reproducible results (0 for random generation) Defaults to 0.
            
            language: Language for synthesis Defaults to 'en'.
            
            cfg_weight: CFG/Pace weight controlling generation guidance (0.2-1.0). Use 0.5 for balanced results, 0 for language transfer Defaults to 0.5.
            
            temperature: Controls randomness in generation (0.05-5.0, higher=more varied) Defaults to 0.8.
            
            exaggeration: Controls speech expressiveness (0.25-2.0, neutral=0.5, extreme values may be unstable) Defaults to 0.5.
            
            reference_audio: Reference audio file for voice cloning (optional). If not provided, uses default voice for the selected language. Optional.
            
        """
        return self.submit_job("/predictions", text=text, seed=seed, language=language, cfg_weight=cfg_weight, temperature=temperature, exaggeration=exaggeration, reference_audio=reference_audio, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions
