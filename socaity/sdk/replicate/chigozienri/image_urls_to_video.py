from fastsdk.fastSDK import FastSDK

class image_urls_to_video(FastSDK):
    """
    Generated client for image_urls_to_video
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="b1ad9b53-ff3e-42ac-b133-968a337508c9", api_key=api_key)
    
    def predict(self, image_urls: str, fps: float = 4.0, mp4: bool = False, output_zip: bool = False, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            image_urls: A comma-separated list of input urls
            
            fps: Frames per second of output video Defaults to 4.0.
            
            mp4: Returns .mp4 if true or .gif if false Defaults to False.
            
            output_zip: Also returns a zip of the input images if true Defaults to False.
            
        """
        return self.submit_job("/predict", image_urls=image_urls, fps=fps, mp4=mp4, output_zip=output_zip, **kwargs)
     