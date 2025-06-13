from fastsdk.fastSDK import FastSDK

class lgm_ply_to_glb(FastSDK):
    """
    Generated client for camenduru/lgm-ply-to-glb
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="67404faa-b95f-4602-8033-815196098913", api_key=api_key)
    
    def predict(self, ply_file_url: str, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            ply_file_url: URL of LGM .ply file
            
        """
        return self.submit_job("/predictions", ply_file_url=ply_file_url, **kwargs)
     