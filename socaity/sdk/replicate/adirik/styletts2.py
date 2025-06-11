from fastsdk.fastSDK import FastSDK
from typing import Optional, Union

from media_toolkit import MediaFile


class styletts2(FastSDK):
    """
    Generated client for styletts2
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="81bbcc03-6aa0-426e-b289-07053d728208", api_key=api_key)
    
    def predict(self, text: str, beta: float = 0.7, seed: int = 0, alpha: float = 0.3, diffusion_steps: int = 10, embedding_scale: float = 1.0, weights: Optional[str] = None, reference: Optional[Union[MediaFile, str, bytes]] = None, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            text: Text to convert to speech
            
            beta: Only used for long text inputs or in case of reference speaker,             determines the prosody of the speaker. Use lower values to sample style based             on previous or reference speech instead of text. Defaults to 0.7.
            
            seed: Seed for reproducibility Defaults to 0.
            
            alpha: Only used for long text inputs or in case of reference speaker,             determines the timbre of the speaker. Use lower values to sample style based             on previous or reference speech instead of text. Defaults to 0.3.
            
            diffusion_steps: Number of diffusion steps Defaults to 10.
            
            embedding_scale: Embedding scale, use higher values for pronounced emotion Defaults to 1.0.
            
            weights: Replicate weights url for inference with model that is fine-tuned on new speakers.            If provided, a reference speech must also be provided.             If not provided, the default model will be used. Optional.
            
            reference: Reference speech to copy style from Optional.
            
        """
        return self.submit_job("/predict", text=text, beta=beta, seed=seed, alpha=alpha, diffusion_steps=diffusion_steps, embedding_scale=embedding_scale, weights=weights, reference=reference, **kwargs)
     