from fastsdk.fastSDK import FastSDK

class whisperx_video_transcribe(FastSDK):
    """
    Generated client for whisperx_video_transcribe
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="706085a7-6a00-4a37-9758-97dedb89a03c", api_key=api_key)
    
    def predict(self, url: str, debug: bool = False, batch_size: int = 16, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            url: Video URL. View supported sites https://dub.sh/supportedsites
            
            debug: Print out memory usage information. Defaults to False.
            
            batch_size: Parallelization of input audio transcription Defaults to 16.
            
        """
        return self.submit_job("/predict", url=url, debug=debug, batch_size=batch_size, **kwargs)
     