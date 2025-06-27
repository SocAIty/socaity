from fastsdk import FastSDK, APISeex

class create_rvc_dataset(FastSDK):
    """
    Generated client for zsxkib/create-rvc-dataset
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="b4229eae-1f48-4adb-bcaf-502aaf304c25", api_key=api_key)
    
    def predictions(self, youtube_url: str, audio_name: str = 'rvc_v2_voices', **kwargs) -> APISeex:
        """
        
        
        
        Args:
            youtube_url: URL to YouTube video you'd like to create your RVC v2 dataset from
            
            audio_name: Name of the dataset. The output will be a zip file containing a folder named `dataset/<audio_name>/`. This folder will include multiple `.mp3` files named as `split_<i>.mp3`. Each `split_<i>.mp3` file is a short audio clip extracted from the provided YouTube video, where voice has been isolated from the background noise. Defaults to 'rvc_v2_voices'.
            
        """
        return self.submit_job("/predictions", youtube_url=youtube_url, audio_name=audio_name, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions