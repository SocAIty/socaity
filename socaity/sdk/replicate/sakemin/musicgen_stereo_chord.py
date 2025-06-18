from fastsdk import FastSDK, APISeex
from typing import Optional, Union

from media_toolkit import MediaFile


class musicgen_stereo_chord(FastSDK):
    """
    Generated client for sakemin/musicgen-stereo-chord
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="4d80c2dc-a76b-447f-bf79-e677161b6d6c", api_key=api_key)
    
    def predictions(self, top_k: int = 250, top_p: float = 0.0, duration: int = 8, time_sig: str = '4/4', audio_start: int = 0, temperature: float = 1.0, continuation: bool = False, model_version: str = 'stereo-chord-large', output_format: str = 'wav', chroma_coefficient: float = 1.0, multi_band_diffusion: bool = False, normalization_strategy: str = 'loudness', classifier_free_guidance: int = 3, bpm: Optional[float] = None, seed: Optional[int] = None, prompt: Optional[str] = None, audio_end: Optional[int] = None, text_chords: Optional[str] = None, audio_chords: Optional[Union[MediaFile, str, bytes]] = None, **kwargs) -> APISeex:
        """
        Run a single prediction on the model
        
        
        Args:
            top_k: Reduces sampling to the k most likely tokens. Defaults to 250.
            
            top_p: Reduces sampling to tokens with cumulative probability of p. When set to  `0` (default), top_k sampling is used. Defaults to 0.0.
            
            duration: Duration of the generated audio in seconds. Defaults to 8.
            
            time_sig: Time signature value for the generate output. `text_chords` will be processed based on this value. This will be appended at the end of `prompt`. Defaults to '4/4'.
            
            audio_start: Start time of the audio file to use for chord conditioning. Defaults to 0.
            
            temperature: Controls the 'conservativeness' of the sampling process. Higher temperature means more diversity. Defaults to 1.0.
            
            continuation: If `True`, generated music will continue from `audio_chords`. If chord conditioning, this is only possible when the chord condition is given with `text_chords`. If `False`, generated music will mimic `audio_chords`'s chord. Defaults to False.
            
            model_version: Model type. Select `fine-tuned` if you trained the model into your own repository. Defaults to 'stereo-chord-large'.
            
            output_format: Output format for generated audio. Defaults to 'wav'.
            
            chroma_coefficient: Coefficient value multiplied to multi-hot chord chroma. Defaults to 1.0.
            
            multi_band_diffusion: If `True`, the EnCodec tokens will be decoded with MultiBand Diffusion. Not compatible with stereo models. Defaults to False.
            
            normalization_strategy: Strategy for normalizing audio. Defaults to 'loudness'.
            
            classifier_free_guidance: Increases the influence of inputs on the output. Higher values produce lower-varience outputs that adhere more closely to inputs. Defaults to 3.
            
            bpm: BPM condition for the generated output. `text_chords` will be processed based on this value. This will be appended at the end of `prompt`. Optional.
            
            seed: Seed for random number generator. If `None` or `-1`, a random seed will be used. Optional.
            
            prompt: A description of the music you want to generate. Optional.
            
            audio_end: End time of the audio file to use for chord conditioning. If None, will default to the end of the audio clip. Optional.
            
            text_chords: A text based chord progression condition. Single uppercase alphabet character(eg. `C`) is considered as a major chord. Chord attributes like(`maj`, `min`, `dim`, `aug`, `min6`, `maj6`, `min7`, `minmaj7`, `maj7`, `7`, `dim7`, `hdim7`, `sus2` and `sus4`) can be added to the root alphabet character after `:`.(eg. `A:min7`) Each chord token splitted by `SPACE` is allocated to a single bar. If more than one chord must be allocated to a single bar, cluster the chords adding with `,` without any `SPACE`.(eg. `C,C:7 G, E:min A:min`) You must choose either only one of `audio_chords` below or `text_chords`. Optional.
            
            audio_chords: An audio file that will condition the chord progression. You must choose only one among `audio_chords` or `text_chords` above. Optional.
            
        """
        return self.submit_job("/predictions", top_k=top_k, top_p=top_p, duration=duration, time_sig=time_sig, audio_start=audio_start, temperature=temperature, continuation=continuation, model_version=model_version, output_format=output_format, chroma_coefficient=chroma_coefficient, multi_band_diffusion=multi_band_diffusion, normalization_strategy=normalization_strategy, classifier_free_guidance=classifier_free_guidance, bpm=bpm, seed=seed, prompt=prompt, audio_end=audio_end, text_chords=text_chords, audio_chords=audio_chords, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions