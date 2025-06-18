from fastsdk import FastSDK, APISeex
from typing import List, Optional, Any, Dict, Union

from media_toolkit import MediaFile


class hunyuan_video2video(FastSDK):
    """
    Generated client for zsxkib/hunyuan-video2video
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="e1e6a6c2-9f32-45a0-94c4-077b5880602e", api_key=api_key)
    
    def trainings(self, webhook_events_filter: Union[List[Any], str] = ['start', 'output', 'logs', 'completed'], id: Optional[str] = None, input: Optional[Dict[str, Any]] = None, webhook: Optional[Union[MediaFile, str, bytes]] = None, created_at: Optional[str] = None, output_file_prefix: Optional[str] = None, **kwargs) -> APISeex:
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
    
    def predictions(self, video: Union[MediaFile, str, bytes], crf: int = 19, steps: int = 30, width: int = 768, height: int = 768, prompt: str = 'high quality nature video of a excited brown bear walking through the grass, masterpiece, best quality', flow_shift: int = 9, force_rate: int = 0, force_size: str = 'Disabled', frame_rate: int = 24, custom_width: int = 512, custom_height: int = 512, frame_load_cap: int = 101, guidance_scale: float = 6.0, keep_proportion: bool = True, denoise_strength: float = 0.85, select_every_nth: int = 1, skip_first_frames: int = 0, seed: Optional[int] = None, **kwargs) -> APISeex:
        """
        Run a single prediction on the model
        
        
        Args:
            video: Input video file.
            
            crf: CRF value for output video quality (0-51). Lower values = better quality. Defaults to 19.
            
            steps: Number of sampling (denoising) steps. Defaults to 30.
            
            width: Output video width (divisible by 16 for best performance). Defaults to 768.
            
            height: Output video height (divisible by 16 for best performance). Defaults to 768.
            
            prompt: Text prompt describing the desired output video style. Be descriptive. Defaults to 'high quality nature video of a excited brown bear walking through the grass, masterpiece, best quality'.
            
            flow_shift: Flow shift for temporal consistency. Adjust to tweak video smoothness. Defaults to 9.
            
            force_rate: Force a new frame rate on the input video. 0 means no change. Defaults to 0.
            
            force_size: Force resize method. 'Disabled' means original size. Otherwise applies custom_width/height. Defaults to 'Disabled'.
            
            frame_rate: Frame rate of the output video. Defaults to 24.
            
            custom_width: Custom width if force_size is not 'Disabled'. Defaults to 512.
            
            custom_height: Custom height if force_size is not 'Disabled'. Defaults to 512.
            
            frame_load_cap: Max frames to load from input video. Defaults to 101.
            
            guidance_scale: Embedded guidance scale. Higher values follow the prompt more strictly. Defaults to 6.0.
            
            keep_proportion: Keep aspect ratio when resizing. If true, will adjust dimensions proportionally. Defaults to True.
            
            denoise_strength: Denoise strength (0.0 to 1.0). Higher = more deviation from input content. Defaults to 0.85.
            
            select_every_nth: Use every nth frame (1 = every frame, 2 = every second frame, etc.). Defaults to 1.
            
            skip_first_frames: Number of initial frames to skip from the input video. Defaults to 0.
            
            seed: Set a seed for reproducibility. Random by default. Optional.
            
        """
        return self.submit_job("/predictions", video=video, crf=crf, steps=steps, width=width, height=height, prompt=prompt, flow_shift=flow_shift, force_rate=force_rate, force_size=force_size, frame_rate=frame_rate, custom_width=custom_width, custom_height=custom_height, frame_load_cap=frame_load_cap, guidance_scale=guidance_scale, keep_proportion=keep_proportion, denoise_strength=denoise_strength, select_every_nth=select_every_nth, skip_first_frames=skip_first_frames, seed=seed, **kwargs)
    
    def trainings_training_id(self, raining_equest: Dict[str, Any], **kwargs) -> APISeex:
        """
        None
        
        
        Args:
            raining_equest: No description available.
            
        """
        return self.submit_job("/trainings/{training_id}", raining_equest=raining_equest, **kwargs)
    
    def trainings_training_id_cancel(self, **kwargs) -> APISeex:
        """
        None
        
        """
        return self.submit_job("/trainings/{training_id}/cancel", **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = trainings
    __call__ = trainings