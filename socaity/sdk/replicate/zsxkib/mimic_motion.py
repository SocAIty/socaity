from fastsdk.fastSDK import FastSDK
from typing import Optional, Union

from media_toolkit import MediaFile


class mimic_motion(FastSDK):
    """
    Generated client for mimic_motion
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="daa13086-1eda-4dfa-ade2-75b252b5ef71", api_key=api_key)
    
    def predict(self, motion_video: Union[MediaFile, str, bytes], appearance_image: Union[MediaFile, str, bytes], chunk_size: int = 16, resolution: int = 576, sample_stride: int = 2, frames_overlap: int = 6, guidance_scale: float = 2.0, noise_strength: float = 0.0, denoising_steps: int = 25, checkpoint_version: str = 'v1-1', output_frames_per_second: int = 15, seed: Optional[int] = None, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            motion_video: Reference video file containing the motion to be mimicked
            
            appearance_image: Reference image file for the appearance of the generated video
            
            chunk_size: Number of frames to generate in each processing chunk Defaults to 16.
            
            resolution: Height of the output video in pixels. Width is automatically calculated. Defaults to 576.
            
            sample_stride: Interval for sampling frames from the reference video. Higher values skip more frames. Defaults to 2.
            
            frames_overlap: Number of overlapping frames between chunks for smoother transitions Defaults to 6.
            
            guidance_scale: Strength of guidance towards the reference. Higher values adhere more closely to the reference but may reduce creativity. Defaults to 2.0.
            
            noise_strength: Strength of noise augmentation. Higher values add more variation but may reduce coherence with the reference. Defaults to 0.0.
            
            denoising_steps: Number of denoising steps in the diffusion process. More steps can improve quality but increase processing time. Defaults to 25.
            
            checkpoint_version: Choose the checkpoint version to use Defaults to 'v1-1'.
            
            output_frames_per_second: Frames per second of the output video. Affects playback speed. Defaults to 15.
            
            seed: Random seed. Leave blank to randomize the seed Optional.
            
        """
        return self.submit_job("/predict", motion_video=motion_video, appearance_image=appearance_image, chunk_size=chunk_size, resolution=resolution, sample_stride=sample_stride, frames_overlap=frames_overlap, guidance_scale=guidance_scale, noise_strength=noise_strength, denoising_steps=denoising_steps, checkpoint_version=checkpoint_version, output_frames_per_second=output_frames_per_second, seed=seed, **kwargs)
     