from fastsdk import FastSDK, APISeex
from typing import Optional, Union

from media_toolkit import MediaFile


class ultimate_sd_upscale(FastSDK):
    """
    Generated client for fewjative/ultimate-sd-upscale
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="3765c151-0f0c-440b-8bf4-f04c6190eaef", api_key=api_key)
    
    def predictions(self, image: Union[str, MediaFile, bytes], cfg: float = 8.0, steps: int = 20, denoise: float = 0.2, upscaler: str = '4x-UltraSharp', mask_blur: int = 8, mode_type: str = 'Linear', scheduler: str = 'normal', tile_width: int = 512, upscale_by: float = 2.0, tile_height: int = 512, sampler_name: str = 'euler', tile_padding: int = 32, seam_fix_mode: str = 'None', seam_fix_width: int = 64, negative_prompt: str = '', positive_prompt: str = 'Hey! Have a nice day :D', seam_fix_denoise: float = 1.0, seam_fix_padding: int = 16, seam_fix_mask_blur: int = 8, controlnet_strength: float = 1.0, force_uniform_tiles: bool = True, use_controlnet_tile: bool = True, seed: Optional[int] = None, **kwargs) -> APISeex:
        """
        
        
        
        Args:
            image: Input image
            
            cfg: CFG Defaults to 8.0.
            
            steps: Steps Defaults to 20.
            
            denoise: Denoise Defaults to 0.2.
            
            upscaler: Upscaler Defaults to '4x-UltraSharp'.
            
            mask_blur: Mask Blur Defaults to 8.
            
            mode_type: Mode Type Defaults to 'Linear'.
            
            scheduler: Scheduler Defaults to 'normal'.
            
            tile_width: Tile Width Defaults to 512.
            
            upscale_by: Upscale By Defaults to 2.0.
            
            tile_height: Tile Height Defaults to 512.
            
            sampler_name: Sampler Defaults to 'euler'.
            
            tile_padding: Tile Padding Defaults to 32.
            
            seam_fix_mode: Seam Fix Mode Defaults to 'None'.
            
            seam_fix_width: Seam Fix Width Defaults to 64.
            
            negative_prompt: Negative Prompt Defaults to ''.
            
            positive_prompt: Positive Prompt Defaults to 'Hey! Have a nice day :D'.
            
            seam_fix_denoise: Seam Fix Denoise Defaults to 1.0.
            
            seam_fix_padding: Seam Fix Padding Defaults to 16.
            
            seam_fix_mask_blur: Seam Fix Mask Blur Defaults to 8.
            
            controlnet_strength: ControlNet Strength Defaults to 1.0.
            
            force_uniform_tiles: Force Uniform Tiles Defaults to True.
            
            use_controlnet_tile: Use ControlNet Tile Defaults to True.
            
            seed: Sampling seed, leave Empty for Random Optional.
            
        """
        return self.submit_job("/predictions", image=image, cfg=cfg, steps=steps, denoise=denoise, upscaler=upscaler, mask_blur=mask_blur, mode_type=mode_type, scheduler=scheduler, tile_width=tile_width, upscale_by=upscale_by, tile_height=tile_height, sampler_name=sampler_name, tile_padding=tile_padding, seam_fix_mode=seam_fix_mode, seam_fix_width=seam_fix_width, negative_prompt=negative_prompt, positive_prompt=positive_prompt, seam_fix_denoise=seam_fix_denoise, seam_fix_padding=seam_fix_padding, seam_fix_mask_blur=seam_fix_mask_blur, controlnet_strength=controlnet_strength, force_uniform_tiles=force_uniform_tiles, use_controlnet_tile=use_controlnet_tile, seed=seed, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions