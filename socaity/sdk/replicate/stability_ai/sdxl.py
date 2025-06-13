from fastsdk.fastSDK import FastSDK
from typing import Any, Union, Dict, List, Optional

from media_toolkit import MediaFile


class sdxl(FastSDK):
    """
    Generated client for stability-ai/sdxl
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="c6f62ea6-7a73-45b7-96fa-d992742b17c3", api_key=api_key)
    
    def trainings(self, webhook_events_filter: Union[List[Any], str] = ['start', 'output', 'logs', 'completed'], id: Optional[str] = None, input: Optional[Dict[str, Any]] = None, webhook: Optional[Union[MediaFile, str, bytes]] = None, created_at: Optional[str] = None, output_file_prefix: Optional[str] = None, **kwargs):
        """
        None
        
        
        Args:
            webhook_events_filter: No description available. Defaults to ['start', 'output', 'logs', 'completed'].
            
            id: No description available. Optional.
            
            input: No description available. Optional.
            
            webhook: No description available. Optional.
            
            created_at: No description available. Optional.
            
            output_file_prefix: No description available. Optional.
            
        """
        return self.submit_job("/trainings", webhook_events_filter=webhook_events_filter, id=id, input=input, webhook=webhook, created_at=created_at, output_file_prefix=output_file_prefix, **kwargs)
    
    def predict(self, width: int = 1024, height: int = 1024, prompt: str = 'An astronaut riding a rainbow unicorn', refine: str = 'no_refiner', scheduler: str = 'K_EULER', lora_scale: float = 0.6, num_outputs: int = 1, guidance_scale: float = 7.5, apply_watermark: bool = True, high_noise_frac: float = 0.8, negative_prompt: str = '', prompt_strength: float = 0.8, num_inference_steps: int = 50, disable_safety_checker: bool = False, mask: Optional[Union[MediaFile, str, bytes]] = None, seed: Optional[int] = None, image: Optional[Union[MediaFile, str, bytes]] = None, refine_steps: Optional[int] = None, replicate_weights: Optional[str] = None, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            width: Width of output image Defaults to 1024.
            
            height: Height of output image Defaults to 1024.
            
            prompt: Input prompt Defaults to 'An astronaut riding a rainbow unicorn'.
            
            refine: Which refine style to use Defaults to 'no_refiner'.
            
            scheduler: scheduler Defaults to 'K_EULER'.
            
            lora_scale: LoRA additive scale. Only applicable on trained models. Defaults to 0.6.
            
            num_outputs: Number of images to output. Defaults to 1.
            
            guidance_scale: Scale for classifier-free guidance Defaults to 7.5.
            
            apply_watermark: Applies a watermark to enable determining if an image is generated in downstream applications. If you have other provisions for generating or deploying images safely, you can use this to disable watermarking. Defaults to True.
            
            high_noise_frac: For expert_ensemble_refiner, the fraction of noise to use Defaults to 0.8.
            
            negative_prompt: Input Negative Prompt Defaults to ''.
            
            prompt_strength: Prompt strength when using img2img / inpaint. 1.0 corresponds to full destruction of information in image Defaults to 0.8.
            
            num_inference_steps: Number of denoising steps Defaults to 50.
            
            disable_safety_checker: Disable safety checker for generated images. This feature is only available through the API. See [https://replicate.com/docs/how-does-replicate-work#safety](https://replicate.com/docs/how-does-replicate-work#safety) Defaults to False.
            
            mask: Input mask for inpaint mode. Black areas will be preserved, white areas will be inpainted. Optional.
            
            seed: Random seed. Leave blank to randomize the seed Optional.
            
            image: Input image for img2img or inpaint mode Optional.
            
            refine_steps: For base_image_refiner, the number of steps to refine, defaults to num_inference_steps Optional.
            
            replicate_weights: Replicate LoRA weights to use. Leave blank to use the default weights. Optional.
            
        """
        return self.submit_job("/predictions", width=width, height=height, prompt=prompt, refine=refine, scheduler=scheduler, lora_scale=lora_scale, num_outputs=num_outputs, guidance_scale=guidance_scale, apply_watermark=apply_watermark, high_noise_frac=high_noise_frac, negative_prompt=negative_prompt, prompt_strength=prompt_strength, num_inference_steps=num_inference_steps, disable_safety_checker=disable_safety_checker, mask=mask, seed=seed, image=image, refine_steps=refine_steps, replicate_weights=replicate_weights, **kwargs)
    
    def trainings_training_id(self, raining_equest: Dict[str, Any], **kwargs):
        """
        None
        
        
        Args:
            raining_equest: No description available.
            
        """
        return self.submit_job("/trainings/{training_id}", raining_equest=raining_equest, **kwargs)
    
    def trainings_training_id_cancel(self, **kwargs):
        """
        None
        
        """
        return self.submit_job("/trainings/{training_id}/cancel", **kwargs)
     