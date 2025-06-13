from fastsdk.fastSDK import FastSDK
from typing import Union, Optional

from media_toolkit import MediaFile


class ai_glasses(FastSDK):
    """
    Generated client for warf23/ai-glasses
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="6daea01c-eebd-4809-871f-a7779c07ed55", api_key=api_key)
    
    def predict(self, prompt: str, model: str = 'dev', go_fast: bool = False, lora_scale: float = 1.0, megapixels: str = '1', num_outputs: int = 1, aspect_ratio: str = '1:1', output_format: str = 'webp', guidance_scale: float = 3.0, output_quality: int = 80, prompt_strength: float = 0.8, extra_lora_scale: float = 1.0, num_inference_steps: int = 28, disable_safety_checker: bool = False, mask: Optional[Union[MediaFile, str, bytes]] = None, seed: Optional[int] = None, image: Optional[Union[MediaFile, str, bytes]] = None, width: Optional[int] = None, height: Optional[int] = None, extra_lora: Optional[str] = None, replicate_weights: Optional[str] = None, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            prompt: Prompt for generated image. If you include the `trigger_word` used in the training process you are more likely to activate the trained object, style, or concept in the resulting image.
            
            model: Which model to run inference with. The dev model performs best with around 28 inference steps but the schnell model only needs 4 steps. Defaults to 'dev'.
            
            go_fast: Run faster predictions with model optimized for speed (currently fp8 quantized); disable to run in original bf16 Defaults to False.
            
            lora_scale: Determines how strongly the main LoRA should be applied. Sane results between 0 and 1 for base inference. For go_fast we apply a 1.5x multiplier to this value; we've generally seen good performance when scaling the base value by that amount. You may still need to experiment to find the best value for your particular lora. Defaults to 1.0.
            
            megapixels: Approximate number of megapixels for generated image Defaults to '1'.
            
            num_outputs: Number of outputs to generate Defaults to 1.
            
            aspect_ratio: Aspect ratio for the generated image. If custom is selected, uses height and width below & will run in bf16 mode Defaults to '1:1'.
            
            output_format: Format of the output images Defaults to 'webp'.
            
            guidance_scale: Guidance scale for the diffusion process. Lower values can give more realistic images. Good values to try are 2, 2.5, 3 and 3.5 Defaults to 3.0.
            
            output_quality: Quality when saving the output images, from 0 to 100. 100 is best quality, 0 is lowest quality. Not relevant for .png outputs Defaults to 80.
            
            prompt_strength: Prompt strength when using img2img. 1.0 corresponds to full destruction of information in image Defaults to 0.8.
            
            extra_lora_scale: Determines how strongly the extra LoRA should be applied. Sane results between 0 and 1 for base inference. For go_fast we apply a 1.5x multiplier to this value; we've generally seen good performance when scaling the base value by that amount. You may still need to experiment to find the best value for your particular lora. Defaults to 1.0.
            
            num_inference_steps: Number of denoising steps. More steps can give more detailed images, but take longer. Defaults to 28.
            
            disable_safety_checker: Disable safety checker for generated images. Defaults to False.
            
            mask: Image mask for image inpainting mode. If provided, aspect_ratio, width, and height inputs are ignored. Optional.
            
            seed: Random seed. Set for reproducible generation Optional.
            
            image: Input image for image to image or inpainting mode. If provided, aspect_ratio, width, and height inputs are ignored. Optional.
            
            width: Width of generated image. Only works if `aspect_ratio` is set to custom. Will be rounded to nearest multiple of 16. Incompatible with fast generation Optional.
            
            height: Height of generated image. Only works if `aspect_ratio` is set to custom. Will be rounded to nearest multiple of 16. Incompatible with fast generation Optional.
            
            extra_lora: Load LoRA weights. Supports Replicate models in the format <owner>/<username> or <owner>/<username>/<version>, HuggingFace URLs in the format huggingface.co/<owner>/<model-name>, CivitAI URLs in the format civitai.com/models/<id>[/<model-name>], or arbitrary .safetensors URLs from the Internet. For example, 'fofr/flux-pixar-cars' Optional.
            
            replicate_weights: Load LoRA weights. Supports Replicate models in the format <owner>/<username> or <owner>/<username>/<version>, HuggingFace URLs in the format huggingface.co/<owner>/<model-name>, CivitAI URLs in the format civitai.com/models/<id>[/<model-name>], or arbitrary .safetensors URLs from the Internet. For example, 'fofr/flux-pixar-cars' Optional.
            
        """
        return self.submit_job("/predictions", prompt=prompt, model=model, go_fast=go_fast, lora_scale=lora_scale, megapixels=megapixels, num_outputs=num_outputs, aspect_ratio=aspect_ratio, output_format=output_format, guidance_scale=guidance_scale, output_quality=output_quality, prompt_strength=prompt_strength, extra_lora_scale=extra_lora_scale, num_inference_steps=num_inference_steps, disable_safety_checker=disable_safety_checker, mask=mask, seed=seed, image=image, width=width, height=height, extra_lora=extra_lora, replicate_weights=replicate_weights, **kwargs)
     