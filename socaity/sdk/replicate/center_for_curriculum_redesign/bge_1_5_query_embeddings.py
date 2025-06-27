from fastsdk import FastSDK, APISeex

class bge_1_5_query_embeddings(FastSDK):
    """
    Generated client for center-for-curriculum-redesign/bge-1-5-query-embeddings
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="0b47f390-cedf-429d-9157-dada4f0b747a", api_key=api_key)
    
    def predictions(self, normalize: bool = True, precision: str = 'full', query_texts: str = '[]', batchtoken_max: float = 200.0, **kwargs) -> APISeex:
        """
        
        
        
        Args:
            normalize: normalizes returned embedding vectors to a magnitude of 1. (default: true, as this model presumes cosine similarity comparisons downstream) Defaults to True.
            
            precision: numerical precision for inference computations. Either full or half. Defaults to a paranoid value of full. You may want to test if 'half' is sufficient for your needs, though regardless you should probably prefer to use the same precision for querying as you do for archiving. Defaults to 'full'.
            
            query_texts: A serialized JSON array of strings you wish to generate *retreival* embeddings for. (note, that you should keep this list short to avoid Replicate response size limitations). Use this to embed short text queries intended for comparison against document text. A vector will be returned corresponding to each line of text in the input array (in order of input). This endpoint will automatically format your query strings for retrieval, you do not need to preprocess them. Defaults to '[]'.
            
            batchtoken_max: You probably don't need to worry about this parameter if you're just getting the embeddings for a handful of queries. This parameter sets the maximumum number of kibiTokens (1 kibiToken = 1024 tokens) to try to stuff into a batch (to avoid out of memory errors but maximize throughput). If the total number of tokens across the flattened list of requested embeddings exceed this value, the list will be split internally and run across multiple forward passes. This will not affect the shape of your output, just the time it takes to run. Defaults to 200.0.
            
        """
        return self.submit_job("/predictions", normalize=normalize, precision=precision, query_texts=query_texts, batchtoken_max=batchtoken_max, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions