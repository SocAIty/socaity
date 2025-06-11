from fastsdk.fastSDK import FastSDK

class lgm_ply_to_glb(FastSDK):
    """
    Generated client for lgm_ply_to_glb
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="97b24af0-dd44-46b4-93b5-31789c61741d", api_key=api_key)
    
    def predict(self, ply_file_url: str, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            ply_file_url: URL of LGM .ply file
            
        """
        return self.submit_job("/predict", ply_file_url=ply_file_url, **kwargs)
     