from fastsdk.fastSDK import FastSDK

class clip_features(FastSDK):
    """
    Generated client for andreasjansson/clip-features
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="c0c833f2-2dc4-43b5-8c2a-09bf8d70c89c", api_key=api_key)
    
    def predict(self, inputs: str = 'a\nb', **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            inputs: Newline-separated inputs. Can either be strings of text or image URIs starting with http[s]:// Defaults to 'a\nb'.
            
        """
        return self.submit_job("/predictions", inputs=inputs, **kwargs)
     