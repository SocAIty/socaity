from fastsdk.fastSDK import FastSDK

class snowflake_arctic_embed_l(FastSDK):
    """
    Generated client for snowflake_arctic_embed_l
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="b5ce741c-7263-401c-872f-ba25da81ff69", api_key=api_key)
    
    def predict(self, prompt: str = 'Snowflake is the Data Cloud!', **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            prompt: Prompt to generate a vector embedding for Defaults to 'Snowflake is the Data Cloud!'.
            
        """
        return self.submit_job("/predict", prompt=prompt, **kwargs)
     