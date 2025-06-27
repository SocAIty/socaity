from fastsdk import FastSDK, APISeex

class music_inpainting_bert(FastSDK):
    """
    Generated client for andreasjansson/music-inpainting-bert
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="91a17309-ccf3-41e6-ab92-93c748f2fdfb", api_key=api_key)
    
    def predictions(self, notes: str, chords: str, seed: int = -1, tempo: int = 120, sample_width: int = 10, time_signature: int = 4, **kwargs) -> APISeex:
        """
        
        
        
        Args:
            notes: Notes in tinynotation, with each bar separated by '|'. Use '?' for bars you want in-painted.
            
            chords: Chords (one chord per bar), with each bar separated by '|'. Use '?' for bars you want in-painted.
            
            seed: Random seed, -1 for random Defaults to -1.
            
            tempo: Tempo (beats per minute) Defaults to 120.
            
            sample_width: Number of potential predictions to sample from. The higher, the more chaotic the output. Defaults to 10.
            
            time_signature: Time signature Defaults to 4.
            
        """
        return self.submit_job("/predictions", notes=notes, chords=chords, seed=seed, tempo=tempo, sample_width=sample_width, time_signature=time_signature, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions