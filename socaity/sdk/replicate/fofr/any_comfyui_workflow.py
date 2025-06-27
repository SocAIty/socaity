from fastsdk import FastSDK, APISeex
from typing import Optional, Union

from media_toolkit import MediaFile


class any_comfyui_workflow(FastSDK):
    """
    Generated client for fofr/any-comfyui-workflow
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="5457afef-4c0d-46df-9f62-cf87a4d8e455", api_key=api_key)
    
    def predictions(self, output_format: str = 'webp', workflow_json: str = '', output_quality: int = 95, randomise_seeds: bool = True, force_reset_cache: bool = False, return_temp_files: bool = False, input_file: Optional[Union[str, MediaFile, bytes]] = None, **kwargs) -> APISeex:
        """
        
        
        
        Args:
            output_format: Format of the output images Defaults to 'webp'.
            
            workflow_json: Your ComfyUI workflow as JSON string or URL. You must use the API version of your workflow. Get it from ComfyUI using 'Save (API format)'. Instructions here: https://github.com/replicate/cog-comfyui Defaults to ''.
            
            output_quality: Quality of the output images, from 0 to 100. 100 is best quality, 0 is lowest quality. Defaults to 95.
            
            randomise_seeds: Automatically randomise seeds (seed, noise_seed, rand_seed) Defaults to True.
            
            force_reset_cache: Force reset the ComfyUI cache before running the workflow. Useful for debugging. Defaults to False.
            
            return_temp_files: Return any temporary files, such as preprocessed controlnet images. Useful for debugging. Defaults to False.
            
            input_file: Input image, video, tar or zip file. Read guidance on workflows and input files here: https://github.com/replicate/cog-comfyui. Alternatively, you can replace inputs with URLs in your JSON workflow and the model will download them. Optional.
            
        """
        return self.submit_job("/predictions", output_format=output_format, workflow_json=workflow_json, output_quality=output_quality, randomise_seeds=randomise_seeds, force_reset_cache=force_reset_cache, return_temp_files=return_temp_files, input_file=input_file, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions