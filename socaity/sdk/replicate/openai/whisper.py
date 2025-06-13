from fastsdk.fastSDK import FastSDK
from typing import Union, Optional

from media_toolkit import MediaFile


class whisper(FastSDK):
    """
    Generated client for openai/whisper
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="6cc28a27-46eb-490e-be58-ce948c221273", api_key=api_key)
    
    def ready(self, **kwargs):
        """
        None
        
        """
        return self.submit_job("/ready", **kwargs)
    
    def predict(self, audio: Union[MediaFile, str, bytes], language: str = 'auto', translate: bool = False, temperature: float = 0.0, transcription: str = 'plain text', suppress_tokens: str = '-1', logprob_threshold: float = -1.0, no_speech_threshold: float = 0.6, condition_on_previous_text: bool = True, compression_ratio_threshold: float = 2.4, temperature_increment_on_fallback: float = 0.2, patience: Optional[float] = None, initial_prompt: Optional[str] = None, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            audio: Audio file
            
            language: Language spoken in the audio, specify 'auto' for automatic language detection Defaults to 'auto'.
            
            translate: Translate the text to English when set to True Defaults to False.
            
            temperature: temperature to use for sampling Defaults to 0.0.
            
            transcription: Choose the format for the transcription Defaults to 'plain text'.
            
            suppress_tokens: comma-separated list of token ids to suppress during sampling; '-1' will suppress most special characters except common punctuations Defaults to '-1'.
            
            logprob_threshold: if the average log probability is lower than this value, treat the decoding as failed Defaults to -1.0.
            
            no_speech_threshold: if the probability of the <|nospeech|> token is higher than this value AND the decoding has failed due to `logprob_threshold`, consider the segment as silence Defaults to 0.6.
            
            condition_on_previous_text: if True, provide the previous output of the model as a prompt for the next window; disabling may make the text inconsistent across windows, but the model becomes less prone to getting stuck in a failure loop Defaults to True.
            
            compression_ratio_threshold: if the gzip compression ratio is higher than this value, treat the decoding as failed Defaults to 2.4.
            
            temperature_increment_on_fallback: temperature to increase when falling back when the decoding fails to meet either of the thresholds below Defaults to 0.2.
            
            patience: optional patience value to use in beam decoding, as in https://arxiv.org/abs/2204.05424, the default (1.0) is equivalent to conventional beam search Optional.
            
            initial_prompt: optional text to provide as a prompt for the first window. Optional.
            
        """
        return self.submit_job("/predictions", audio=audio, language=language, translate=translate, temperature=temperature, transcription=transcription, suppress_tokens=suppress_tokens, logprob_threshold=logprob_threshold, no_speech_threshold=no_speech_threshold, condition_on_previous_text=condition_on_previous_text, compression_ratio_threshold=compression_ratio_threshold, temperature_increment_on_fallback=temperature_increment_on_fallback, patience=patience, initial_prompt=initial_prompt, **kwargs)
     