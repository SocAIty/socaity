from fastsdk.fastSDK import FastSDK

class cantable_diffuguesion(FastSDK):
    """
    Generated client for cantable_diffuguesion
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="2715d6bd-5416-4381-808e-62f480913f22", api_key=api_key)
    
    def predict(self, seed: int = -1, tempo: float = 90.0, melody: str = '', duration: int = 32, return_mp3: bool = True, return_midi: bool = True, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            seed: Random seed. Random if seed == -1 Defaults to -1.
            
            tempo: Tempo in quarter notes per minute Defaults to 90.0.
            
            melody: Melody in tinyNotation format. Accepts ? for inpainting a single note, and ?* for inpainting between two melodic parts Defaults to ''.
            
            duration: Duration in quarter notes Defaults to 32.
            
            return_mp3: Return mp3 audio Defaults to True.
            
            return_midi: Return midi Defaults to True.
            
        """
        return self.submit_job("/predict", seed=seed, tempo=tempo, melody=melody, duration=duration, return_mp3=return_mp3, return_midi=return_midi, **kwargs)
     