from fastsdk import FastSDK, APISeex

class stable_diffusion_infinite_zoom(FastSDK):
    """
    Generated client for arielreplicate/stable-diffusion-infinite-zoom
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="94ff68a1-11b2-4672-94ba-30572855ba8a", api_key=api_key)
    
    def predictions(self, prompt: str, inpaint_iter: int = 2, output_format: str = 'mp4', **kwargs) -> APISeex:
        """
        
        
        
        Args:
            prompt: Prompt
            
            inpaint_iter: Number of iterations of pasting the image in it's center and inpainting the boarders Defaults to 2.
            
            output_format: infinite loop gif or mp4 video Defaults to 'mp4'.
            
        """
        return self.submit_job("/predictions", prompt=prompt, inpaint_iter=inpaint_iter, output_format=output_format, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions