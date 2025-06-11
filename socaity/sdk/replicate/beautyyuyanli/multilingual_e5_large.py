from fastsdk.fastSDK import FastSDK

class multilingual_e5_large(FastSDK):
    """
    Generated client for multilingual_e5_large
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="b255f253-2f3c-498d-9485-b543d90eac41", api_key=api_key)
    
    def predict(self, texts: str = '["In the water, fish are swimming.", "Fish swim in the water.", "A book lies open on the table."]', batch_size: int = 32, normalize_embeddings: bool = True, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            texts: text to embed, formatted as JSON list of strings (e.g. ["hello", "world"]) Defaults to '["In the water, fish are swimming.", "Fish swim in the water.", "A book lies open on the table."]'.
            
            batch_size: Batch size to use when processing text data. Defaults to 32.
            
            normalize_embeddings: Whether to normalize embeddings. Defaults to True.
            
        """
        return self.submit_job("/predict", texts=texts, batch_size=batch_size, normalize_embeddings=normalize_embeddings, **kwargs)
     