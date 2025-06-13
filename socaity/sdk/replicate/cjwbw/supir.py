from fastsdk.fastSDK import FastSDK
from typing import Union, Optional

from media_toolkit import MediaFile


class supir(FastSDK):
    """
    Generated client for cjwbw/supir
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="05ee9d66-1243-46d8-92c8-6cd343820df4", api_key=api_key)
    
    def predict(self, image: Union[MediaFile, str, bytes], s_cfg: float = 7.5, s_churn: float = 5.0, s_noise: float = 1.003, upscale: int = 1, a_prompt: str = 'Cinematic, High Contrast, highly detailed, taken using a Canon EOS R camera, hyper detailed photo - realistic maximum detail, 32k, Color Grading, ultra HD, extreme meticulous detailing, skin pore detailing, hyper sharpness, perfect without deformations.', min_size: float = 1024.0, n_prompt: str = 'painting, oil painting, illustration, drawing, art, sketch, oil painting, cartoon, CG Style, 3D render, unreal engine, blurring, dirty, messy, worst quality, low quality, frames, watermark, signature, jpeg artifacts, deformed, lowres, over-smooth', s_stage1: int = -1, s_stage2: float = 1.0, edm_steps: int = 50, use_llava: bool = True, linear: bool = False, model_name: str = 'SUPIR-v0Q', color_fix_type: str = 'Wavelet', spt_linear: float = 1.0, linear_s_stage2: bool = False, spt_linear_s_stage2: float = 0.0, seed: Optional[int] = None, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            image: Low quality input image.
            
            s_cfg:  Classifier-free guidance scale for prompts. Defaults to 7.5.
            
            s_churn: Original churn hy-param of EDM. Defaults to 5.0.
            
            s_noise: Original noise hy-param of EDM. Defaults to 1.003.
            
            upscale: Upsampling ratio of given inputs. Defaults to 1.
            
            a_prompt: Additive positive prompt for the inputs. Defaults to 'Cinematic, High Contrast, highly detailed, taken using a Canon EOS R camera, hyper detailed photo - realistic maximum detail, 32k, Color Grading, ultra HD, extreme meticulous detailing, skin pore detailing, hyper sharpness, perfect without deformations.'.
            
            min_size: Minimum resolution of output images. Defaults to 1024.0.
            
            n_prompt: Negative prompt for the inputs. Defaults to 'painting, oil painting, illustration, drawing, art, sketch, oil painting, cartoon, CG Style, 3D render, unreal engine, blurring, dirty, messy, worst quality, low quality, frames, watermark, signature, jpeg artifacts, deformed, lowres, over-smooth'.
            
            s_stage1: Control Strength of Stage1 (negative means invalid). Defaults to -1.
            
            s_stage2: Control Strength of Stage2. Defaults to 1.0.
            
            edm_steps: Number of steps for EDM Sampling Schedule. Defaults to 50.
            
            use_llava: Use LLaVA model to get captions. Defaults to True.
            
            linear: Linearly (with sigma) increase CFG from 'spt_linear_CFG' to s_cfg. Defaults to False.
            
            model_name: Choose a model. SUPIR-v0Q is the default training settings with paper. SUPIR-v0F is high generalization and high image quality in most cases. Training with light degradation settings. Stage1 encoder of SUPIR-v0F remains more details when facing light degradations. Defaults to 'SUPIR-v0Q'.
            
            color_fix_type: Color Fixing Type.. Defaults to 'Wavelet'.
            
            spt_linear: Start point of linearly increasing CFG. Defaults to 1.0.
            
            linear_s_stage2: Linearly (with sigma) increase s_stage2 from 'spt_linear_s_stage2' to s_stage2. Defaults to False.
            
            spt_linear_s_stage2: Start point of linearly increasing s_stage2. Defaults to 0.0.
            
            seed: Random seed. Leave blank to randomize the seed Optional.
            
        """
        return self.submit_job("/predictions", image=image, s_cfg=s_cfg, s_churn=s_churn, s_noise=s_noise, upscale=upscale, a_prompt=a_prompt, min_size=min_size, n_prompt=n_prompt, s_stage1=s_stage1, s_stage2=s_stage2, edm_steps=edm_steps, use_llava=use_llava, linear=linear, model_name=model_name, color_fix_type=color_fix_type, spt_linear=spt_linear, linear_s_stage2=linear_s_stage2, spt_linear_s_stage2=spt_linear_s_stage2, seed=seed, **kwargs)
     