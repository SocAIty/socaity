from fastsdk.fastSDK import FastSDK

class stable_diffusion_infinite_zoom(FastSDK):
    """
    Generated client for stable_diffusion_infinite_zoom
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="49e33acb-2097-4601-943c-03527c94282d", api_key=api_key)
    
    def predict(self, prompt: str, inpaint_iter: int = 2, output_format: str = 'mp4', **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            prompt: Prompt
            
            inpaint_iter: Number of iterations of pasting the image in it's center and inpainting the boarders Defaults to 2.
            
            output_format: infinite loop gif or mp4 video Defaults to 'mp4'.
            
        """
        return self.submit_job("/predict", prompt=prompt, inpaint_iter=inpaint_iter, output_format=output_format, **kwargs)
     