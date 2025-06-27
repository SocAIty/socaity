from fastsdk import FastSDK, APISeex
from typing import Optional, Union

from media_toolkit import MediaFile


class hunyuan3d_2mv(FastSDK):
    """
    Generated client for tencent/hunyuan3d-2mv
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="2dbbfde1-d700-46b5-b932-0e7f26ed309b", api_key=api_key)
    
    def predictions(self, front_image: Union[str, MediaFile, bytes], seed: int = 1234, steps: int = 30, file_type: str = 'glb', num_chunks: int = 200000, guidance_scale: float = 5.0, randomize_seed: bool = True, target_face_num: int = 10000, octree_resolution: int = 256, remove_background: bool = True, back_image: Optional[Union[str, MediaFile, bytes]] = None, left_image: Optional[Union[str, MediaFile, bytes]] = None, right_image: Optional[Union[str, MediaFile, bytes]] = None, **kwargs) -> APISeex:
        """
        
        
        
        Args:
            front_image: Front view image
            
            seed: Random seed Defaults to 1234.
            
            steps: Number of inference steps Defaults to 30.
            
            file_type: Output file type Defaults to 'glb'.
            
            num_chunks: Number of chunks Defaults to 200000.
            
            guidance_scale: Guidance scale Defaults to 5.0.
            
            randomize_seed: Randomize seed Defaults to True.
            
            target_face_num: Target number of faces for mesh simplification Defaults to 10000.
            
            octree_resolution: Octree resolution Defaults to 256.
            
            remove_background: Remove image background Defaults to True.
            
            back_image: Back view image Optional.
            
            left_image: Left view image Optional.
            
            right_image: Right view image Optional.
            
        """
        return self.submit_job("/predictions", front_image=front_image, seed=seed, steps=steps, file_type=file_type, num_chunks=num_chunks, guidance_scale=guidance_scale, randomize_seed=randomize_seed, target_face_num=target_face_num, octree_resolution=octree_resolution, remove_background=remove_background, back_image=back_image, left_image=left_image, right_image=right_image, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions