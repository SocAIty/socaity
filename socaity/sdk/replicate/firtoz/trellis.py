from fastsdk.fastSDK import FastSDK
from typing import List, Union, Any

from media_toolkit import MediaFile


class trellis(FastSDK):
    """
    Generated client for trellis
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="3c5c4012-3e7c-48de-ab9f-4a9332e9a879", api_key=api_key)
    
    def predict(self, images: Union[List[Any], MediaFile, str, bytes], seed: int = 0, texture_size: int = 1024, mesh_simplify: float = 0.95, generate_color: bool = True, generate_model: bool = False, randomize_seed: bool = True, generate_normal: bool = False, save_gaussian_ply: bool = False, ss_sampling_steps: int = 12, slat_sampling_steps: int = 12, return_no_background: bool = False, ss_guidance_strength: float = 7.5, slat_guidance_strength: float = 3.0, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            images: List of input images to generate 3D asset from
            
            seed: Random seed for generation Defaults to 0.
            
            texture_size: GLB Extraction - Texture Size (only used if generate_model=True) Defaults to 1024.
            
            mesh_simplify: GLB Extraction - Mesh Simplification (only used if generate_model=True) Defaults to 0.95.
            
            generate_color: Generate color video render Defaults to True.
            
            generate_model: Generate 3D model file (GLB) Defaults to False.
            
            randomize_seed: Randomize seed Defaults to True.
            
            generate_normal: Generate normal video render Defaults to False.
            
            save_gaussian_ply: Save Gaussian point cloud as PLY file Defaults to False.
            
            ss_sampling_steps: Stage 1: Sparse Structure Generation - Sampling Steps Defaults to 12.
            
            slat_sampling_steps: Stage 2: Structured Latent Generation - Sampling Steps Defaults to 12.
            
            return_no_background: Return the preprocessed images without background Defaults to False.
            
            ss_guidance_strength: Stage 1: Sparse Structure Generation - Guidance Strength Defaults to 7.5.
            
            slat_guidance_strength: Stage 2: Structured Latent Generation - Guidance Strength Defaults to 3.0.
            
        """
        return self.submit_job("/predict", images=images, seed=seed, texture_size=texture_size, mesh_simplify=mesh_simplify, generate_color=generate_color, generate_model=generate_model, randomize_seed=randomize_seed, generate_normal=generate_normal, save_gaussian_ply=save_gaussian_ply, ss_sampling_steps=ss_sampling_steps, slat_sampling_steps=slat_sampling_steps, return_no_background=return_no_background, ss_guidance_strength=ss_guidance_strength, slat_guidance_strength=slat_guidance_strength, **kwargs)
     