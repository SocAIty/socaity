from fastsdk import FastSDK, APISeex

class multilingual_e5_large(FastSDK):
    """
    Generated client for beautyyuyanli/multilingual-e5-large
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="bc6eeb4f-c584-46a4-a49d-ec6aa4fdd21b", api_key=api_key)
    
    def predictions(self, texts: str = '["In the water, fish are swimming.", "Fish swim in the water.", "A book lies open on the table."]', batch_size: int = 32, normalize_embeddings: bool = True, **kwargs) -> APISeex:
        """
        Run a single prediction on the model
        
        
        Args:
            texts: text to embed, formatted as JSON list of strings (e.g. ["hello", "world"]) Defaults to '["In the water, fish are swimming.", "Fish swim in the water.", "A book lies open on the table."]'.
            
            batch_size: Batch size to use when processing text data. Defaults to 32.
            
            normalize_embeddings: Whether to normalize embeddings. Defaults to True.
            
        """
        return self.submit_job("/predictions", texts=texts, batch_size=batch_size, normalize_embeddings=normalize_embeddings, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions