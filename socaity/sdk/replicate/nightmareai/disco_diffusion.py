from fastsdk.fastSDK import FastSDK
from typing import Optional, Union

from media_toolkit import MediaFile


class disco_diffusion(FastSDK):
    """
    Generated client for disco_diffusion
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="7cdaaa38-4bb2-4d12-9cd4-92b8e0f80331", api_key=api_key)
    
    def predict(self, _50: bool = True, _101: bool = False, steps: int = 100, width: int = 1280, _50x4: bool = False, i_16: bool = True, i_32: bool = True, i_14: bool = False, height: int = 768, prompt: str = 'A beautiful painting of a singular lighthouse, shining its light across a tumultuous sea of blood by greg rutkowski and thomas kinkade, Trending on artstation.', _50x16: bool = False, _50x64: bool = False, _50x101: bool = False, tv_scale: int = 0, sat_scale: int = 0, skip_augs: bool = False, _50_cc12m: bool = False, i_14_336: bool = False, init_scale: int = 1000, skip_steps: int = 10, range_scale: int = 150, cutn_batches: int = 4, display_rate: int = 20, target_scale: int = 20000, _101_yfcc15m: bool = False, _50_yffcc15m: bool = False, diffusion_model: str = '512x512_diffusion_uncond_finetune_008100', i_32_laion2b_e16: bool = False, clip_guidance_scale: int = 5000, use_secondary_model: bool = True, _50_quickgelu_cc12m: bool = False, i_16_laion400m_e31: bool = False, i_16_laion400m_e32: bool = False, i_32_laion400m_e31: bool = False, i_32_laion400m_e32: bool = False, _50_quickgelu_yfcc15m: bool = False, _101_quickgelu_yfcc15m: bool = False, diffusion_sampling_mode: str = 'ddim', i_32quickgelu_laion400m_e31: bool = False, i_32quickgelu_laion400m_e32: bool = False, seed: Optional[int] = None, init_image: Optional[Union[MediaFile, str, bytes]] = None, target_image: Optional[Union[MediaFile, str, bytes]] = None, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            _50: Use RN50 model Defaults to True.
            
            _101: Use RN101 model Defaults to False.
            
            steps: Number of steps, higher numbers will give more refined output but will take longer Defaults to 100.
            
            width: Width of the output image, higher numbers will take longer Defaults to 1280.
            
            _50x4: Use RN50x4 model Defaults to False.
            
            i_16: Use ViTB16 model Defaults to True.
            
            i_32: Use ViTB32 model Defaults to True.
            
            i_14: Use ViTB14 model Defaults to False.
            
            height: Height of the output image, higher numbers will take longer Defaults to 768.
            
            prompt: Text Prompt Defaults to 'A beautiful painting of a singular lighthouse, shining its light across a tumultuous sea of blood by greg rutkowski and thomas kinkade, Trending on artstation.'.
            
            _50x16: Use RN50x16 model Defaults to False.
            
            _50x64: Use RN50x64 model Defaults to False.
            
            _50x101: Use RN50x101 model Defaults to False.
            
            tv_scale: TV Scale Defaults to 0.
            
            sat_scale: Saturation Scale Defaults to 0.
            
            skip_augs: Skip Augmentations Defaults to False.
            
            _50_cc12m: Use RN50_cc12m model Defaults to False.
            
            i_14_336: Use ViTL14_336 model Defaults to False.
            
            init_scale: Initial Scale Defaults to 1000.
            
            skip_steps: Skip Steps Defaults to 10.
            
            range_scale: Range Scale Defaults to 150.
            
            cutn_batches: Cut Batches Defaults to 4.
            
            display_rate: Steps between outputs, lower numbers may slow down generation. Defaults to 20.
            
            target_scale: Target Scale Defaults to 20000.
            
            _101_yfcc15m: Use RN101_yfcc15m model Defaults to False.
            
            _50_yffcc15m: Use RN50_yffcc15m model Defaults to False.
            
            diffusion_model: Diffusion Model Defaults to '512x512_diffusion_uncond_finetune_008100'.
            
            i_32_laion2b_e16: Use ViTB32_laion2b_e16 model Defaults to False.
            
            clip_guidance_scale: CLIP Guidance Scale Defaults to 5000.
            
            use_secondary_model: Use secondary model Defaults to True.
            
            _50_quickgelu_cc12m: Use RN50_quickgelu_cc12m model Defaults to False.
            
            i_16_laion400m_e31: Use ViTB16_laion400m_e31 model Defaults to False.
            
            i_16_laion400m_e32: Use ViTB16_laion400m_e32 model Defaults to False.
            
            i_32_laion400m_e31: Use ViTB32_laion400m_e31 model Defaults to False.
            
            i_32_laion400m_e32: Use ViTB32_laion400m_e32 model Defaults to False.
            
            _50_quickgelu_yfcc15m: Use RN50_quickgelu_yfcc15m model Defaults to False.
            
            _101_quickgelu_yfcc15m: Use RN101_quickgelu_yfcc15m model Defaults to False.
            
            diffusion_sampling_mode: Diffusion Sampling Mode Defaults to 'ddim'.
            
            i_32quickgelu_laion400m_e31: Use ViTB32quickgelu_laion400m_e31 model Defaults to False.
            
            i_32quickgelu_laion400m_e32: Use ViTB32quickgelu_laion400m_e32 model Defaults to False.
            
            seed: Seed (leave empty to use a random seed) Optional.
            
            init_image: Initial image to start generation from Optional.
            
            target_image: Target image to generate towards, similarly to the text prompt Optional.
            
        """
        return self.submit_job("/predict", _50=_50, _101=_101, steps=steps, width=width, _50x4=_50x4, i_16=i_16, i_32=i_32, i_14=i_14, height=height, prompt=prompt, _50x16=_50x16, _50x64=_50x64, _50x101=_50x101, tv_scale=tv_scale, sat_scale=sat_scale, skip_augs=skip_augs, _50_cc12m=_50_cc12m, i_14_336=i_14_336, init_scale=init_scale, skip_steps=skip_steps, range_scale=range_scale, cutn_batches=cutn_batches, display_rate=display_rate, target_scale=target_scale, _101_yfcc15m=_101_yfcc15m, _50_yffcc15m=_50_yffcc15m, diffusion_model=diffusion_model, i_32_laion2b_e16=i_32_laion2b_e16, clip_guidance_scale=clip_guidance_scale, use_secondary_model=use_secondary_model, _50_quickgelu_cc12m=_50_quickgelu_cc12m, i_16_laion400m_e31=i_16_laion400m_e31, i_16_laion400m_e32=i_16_laion400m_e32, i_32_laion400m_e31=i_32_laion400m_e31, i_32_laion400m_e32=i_32_laion400m_e32, _50_quickgelu_yfcc15m=_50_quickgelu_yfcc15m, _101_quickgelu_yfcc15m=_101_quickgelu_yfcc15m, diffusion_sampling_mode=diffusion_sampling_mode, i_32quickgelu_laion400m_e31=i_32quickgelu_laion400m_e31, i_32quickgelu_laion400m_e32=i_32quickgelu_laion400m_e32, seed=seed, init_image=init_image, target_image=target_image, **kwargs)
     