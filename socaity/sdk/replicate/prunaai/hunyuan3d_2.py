from fastsdk import FastSDK, APISeex
from typing import Optional, Union

from media_toolkit import MediaFile


class hunyuan3d_2(FastSDK):
    """
    Generated client for prunaai/hunyuan3d-2
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="2060f890-7195-46af-af4c-ec0b8af12030", api_key=api_key)
    
    def predictions(self, file_type: str = 'glb', face_count: int = 40000, num_chunks: int = 20000, speed_mode: str = 'Juiced 🔥 (fast)', generator_seed: int = 12345, octree_resolution: int = 200, num_inference_steps: int = 50, image_path: Optional[Union[str, MediaFile, bytes]] = None, **kwargs) -> APISeex:
        """
        
        
        
        Args:
            file_type: File type Defaults to 'glb'.
            
            face_count: Target number of faces for simplification Defaults to 40000.
            
            num_chunks: Number of chunks Defaults to 20000.
            
            speed_mode: Speed optimization level Defaults to 'Juiced 🔥 (fast)'.
            
            generator_seed: Seed for random generator Defaults to 12345.
            
            octree_resolution: Octree resolution Defaults to 200.
            
            num_inference_steps: Number of inference steps Defaults to 50.
            
            image_path: Input image for hunyuan3d control Optional.
            
        """
        return self.submit_job("/predictions", file_type=file_type, face_count=face_count, num_chunks=num_chunks, speed_mode=speed_mode, generator_seed=generator_seed, octree_resolution=octree_resolution, num_inference_steps=num_inference_steps, image_path=image_path, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions