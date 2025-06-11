from fastsdk.fastSDK import FastSDK

class create_rvc_dataset(FastSDK):
    """
    Generated client for create_rvc_dataset
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="c732f35f-04ad-4355-8be0-598def733ede", api_key=api_key)
    
    def predict(self, youtube_url: str, audio_name: str = 'rvc_v2_voices', **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            youtube_url: URL to YouTube video you'd like to create your RVC v2 dataset from
            
            audio_name: Name of the dataset. The output will be a zip file containing a folder named `dataset/<audio_name>/`. This folder will include multiple `.mp3` files named as `split_<i>.mp3`. Each `split_<i>.mp3` file is a short audio clip extracted from the provided YouTube video, where voice has been isolated from the background noise. Defaults to 'rvc_v2_voices'.
            
        """
        return self.submit_job("/predict", youtube_url=youtube_url, audio_name=audio_name, **kwargs)
     