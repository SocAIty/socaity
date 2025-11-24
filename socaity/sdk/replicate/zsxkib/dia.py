from fastsdk import FastClient, APISeex
from typing import Optional

from media_toolkit import MediaFile


class dia(FastClient):
    """
    Generated client based on zsxkib/dia format
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="5c18ced9-4670-4185-874b-64b8877e9fd1", api_key=api_key)
    
    def predictions(self, text: str, seed: int = 42, top_p: float = 0.95, cfg_scale: float = 3.0, temperature: float = 1.8, speed_factor: float = 1.0, max_new_tokens: int = 3072, cfg_filter_top_k: int = 45, max_audio_prompt_seconds: int = 10, audio_prompt: Optional[MediaFile] = None, audio_prompt_text: Optional[str] = None, **kwargs) -> APISeex:
        """
        
        
        
        Args:
            text: Input text for dialogue generation. Use [S1], [S2] to indicate different speakers and (description) in parentheses for non-verbal cues e.g., (laughs), (whispers).
            
            seed: Random seed for reproducible results. Use the same seed value to get the same output for identical inputs. Leave blank for random results each time. Defaults to 42.
            
            top_p: Controls diversity of word choice. Higher values include more unusual options. Most users shouldn't need to adjust this parameter. Defaults to 0.95.
            
            cfg_scale: Controls how closely the audio follows your text. Higher values (3-5) follow text more strictly; lower values may sound more natural but deviate more. Defaults to 3.0.
            
            temperature: Controls randomness in generation. Higher values (1.3-2.0) increase variety; lower values make output more consistent. Set to 0 for deterministic (greedy) generation. Defaults to 1.8.
            
            speed_factor: Adjusts playback speed of the generated audio. Values below 1.0 slow down the audio; 1.0 is original speed. Defaults to 1.0.
            
            max_new_tokens: Controls the length of generated audio. Higher values create longer audio. (86 tokens ≈ 1 second of audio). Defaults to 3072.
            
            cfg_filter_top_k: Technical parameter for filtering audio generation tokens. Higher values allow more diverse sounds; lower values create more consistent audio. Defaults to 45.
            
            max_audio_prompt_seconds: Maximum duration in seconds for the input voice cloning audio prompt. Only used when an audio prompt is provided. Longer voice samples will be truncated to this length. Defaults to 10.
            
            audio_prompt: Optional audio file (.wav/.mp3/.flac) for voice cloning. The model will attempt to mimic this voice style. Optional.
            
            audio_prompt_text: Optional transcript of the audio prompt. If provided, this will be prepended to the main text input. Optional.
            
        """
        return self.submit_job("/predictions", text=text, seed=seed, top_p=top_p, cfg_scale=cfg_scale, temperature=temperature, speed_factor=speed_factor, max_new_tokens=max_new_tokens, cfg_filter_top_k=cfg_filter_top_k, max_audio_prompt_seconds=max_audio_prompt_seconds, audio_prompt=audio_prompt, audio_prompt_text=audio_prompt_text, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions
