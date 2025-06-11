from fastsdk.fastSDK import FastSDK
from typing import Optional, Union

from media_toolkit import MediaFile


class stable_video_face_restoration(FastSDK):
    """
    Generated client for stable_video_face_restoration
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="e7c947c5-04bc-4b2b-b9b7-70cf7672f003", api_key=api_key)
    
    def predict(self, video: Union[MediaFile, str, bytes], tasks: str = 'face-restoration', overlap: int = 3, decode_chunk_size: int = 16, i2i_noise_strength: float = 1.0, noise_aug_strength: float = 0.0, num_inference_steps: int = 30, max_appearance_guidance_scale: float = 2.0, min_appearance_guidance_scale: float = 2.0, mask: Optional[Union[MediaFile, str, bytes]] = None, seed: Optional[int] = None, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            video: Input video file (e.g. MP4).
            
            tasks: Which restoration tasks to apply. Defaults to 'face-restoration'.
            
            overlap: Number of overlapping frames between segments. Defaults to 3.
            
            decode_chunk_size: Chunk size for decoding long videos. Defaults to 16.
            
            i2i_noise_strength: Image-to-image noise strength. Defaults to 1.0.
            
            noise_aug_strength: Noise augmentation strength. Defaults to 0.0.
            
            num_inference_steps: Number of diffusion steps. Defaults to 30.
            
            max_appearance_guidance_scale: Maximum guidance scale for restoration. Defaults to 2.0.
            
            min_appearance_guidance_scale: Minimum guidance scale for restoration. Defaults to 2.0.
            
            mask: An inpainting mask image (white areas will be restored). Only required when tasks includes inpainting. Optional.
            
            seed: Random seed. Leave blank to randomize. Optional.
            
        """
        return self.submit_job("/predict", video=video, tasks=tasks, overlap=overlap, decode_chunk_size=decode_chunk_size, i2i_noise_strength=i2i_noise_strength, noise_aug_strength=noise_aug_strength, num_inference_steps=num_inference_steps, max_appearance_guidance_scale=max_appearance_guidance_scale, min_appearance_guidance_scale=min_appearance_guidance_scale, mask=mask, seed=seed, **kwargs)
     