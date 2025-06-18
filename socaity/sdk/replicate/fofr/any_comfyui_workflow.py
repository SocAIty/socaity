from fastsdk import FastSDK, APISeex
from typing import Dict, List, Union, Any, Optional

from media_toolkit import MediaFile


class any_comfyui_workflow(FastSDK):
    """
    Generated client for fofr/any-comfyui-workflow
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="5457afef-4c0d-46df-9f62-cf87a4d8e455", api_key=api_key)
    
    def trainings(self, webhook_events_filter: Union[List[Any], str] = ['start', 'output', 'logs', 'completed'], id: Optional[str] = None, input: Optional[Dict[str, Any]] = None, context: Optional[Dict[str, Any]] = None, webhook: Optional[Union[MediaFile, str, bytes]] = None, created_at: Optional[str] = None, output_file_prefix: Optional[str] = None, **kwargs) -> APISeex:
        """
        None
        
        
        Args:
            webhook_events_filter: No description available. Defaults to ['start', 'output', 'logs', 'completed'].
            
            id: No description available. Optional.
            
            input: No description available. Optional.
            
            context: No description available. Optional.
            
            webhook: No description available. Optional.
            
            created_at: No description available. Optional.
            
            output_file_prefix: No description available. Optional.
            
        """
        return self.submit_job("/trainings", webhook_events_filter=webhook_events_filter, id=id, input=input, context=context, webhook=webhook, created_at=created_at, output_file_prefix=output_file_prefix, **kwargs)
    
    def predictions(self, output_format: str = 'webp', workflow_json: str = '', output_quality: int = 95, randomise_seeds: bool = True, force_reset_cache: bool = False, return_temp_files: bool = False, input_file: Optional[Union[MediaFile, str, bytes]] = None, **kwargs) -> APISeex:
        """
        Run a single prediction on the model
        
        
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
    
    def trainings_training_id(self, webhook_events_filter: Union[List[Any], str] = ['start', 'output', 'logs', 'completed'], id: Optional[str] = None, input: Optional[Dict[str, Any]] = None, context: Optional[Dict[str, Any]] = None, webhook: Optional[Union[MediaFile, str, bytes]] = None, created_at: Optional[str] = None, output_file_prefix: Optional[str] = None, **kwargs) -> APISeex:
        """
        None
        
        
        Args:
            webhook_events_filter: No description available. Defaults to ['start', 'output', 'logs', 'completed'].
            
            id: No description available. Optional.
            
            input: No description available. Optional.
            
            context: No description available. Optional.
            
            webhook: No description available. Optional.
            
            created_at: No description available. Optional.
            
            output_file_prefix: No description available. Optional.
            
        """
        return self.submit_job("/trainings/{training_id}", webhook_events_filter=webhook_events_filter, id=id, input=input, context=context, webhook=webhook, created_at=created_at, output_file_prefix=output_file_prefix, **kwargs)
    
    def trainings_training_id_cancel(self, **kwargs) -> APISeex:
        """
        None
        
        """
        return self.submit_job("/trainings/{training_id}/cancel", **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = trainings
    __call__ = trainings