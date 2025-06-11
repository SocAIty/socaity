from fastsdk.fastSDK import FastSDK

class clip_features(FastSDK):
    """
    Generated client for clip_features
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="d2246d10-cdc5-4d4e-8300-6d645142b830", api_key=api_key)
    
    def predict(self, inputs: str = 'a\nb', **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            inputs: Newline-separated inputs. Can either be strings of text or image URIs starting with http[s]:// Defaults to 'a\nb'.
            
        """
        return self.submit_job("/predict", inputs=inputs, **kwargs)
     