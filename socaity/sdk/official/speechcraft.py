from fastsdk import FastSDK, APISeex
from typing import Any, Union

from media_toolkit import AudioFile, MediaFile


class speechcraft(FastSDK):
    """
    Create audio from text, clone voices and use them. Convert voice2voice. Generative text-to-audio Bark model.
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="ee0af319-70d4-4171-9954-c24ad01b3e05", api_key=api_key)
    
    def health(self, **kwargs) -> APISeex:
        """
        Get server health status.
        
        Returns:
            HTTP response with health status
        
        """
        return self.submit_job("/health", **kwargs)
    
    def status(self, job_id: str, return_format: str = 'json', keep_alive: bool = False, **kwargs) -> APISeex:
        """
        Get the status and result of a job.
        
        Args:
            job_id: The ID of the job
            return_format: Response format ('json' or 'gzipped')
            keep_alive: If True, job result is kept in memory/disk
        
        Returns:
            JobResult with status and results
        
        """
        return self.submit_job("/status", job_id=job_id, return_format=return_format, keep_alive=keep_alive, **kwargs)
    
    def text2voice(self, text: str, voice: Union[str, MediaFile, Any, bytes] = 'en_speaker_3', fine_temp: float = 0.5, coarse_temp: float = 0.7, coarse_top_k: int = 50, coarse_top_p: float = 0.95, semantic_temp: float = 0.7, semantic_top_k: int = 50, semantic_top_p: float = 0.95, **kwargs) -> APISeex:
        """
        :param text: the text to be converted
        :param voice: the name of the voice to be used. Uses the pretrained voices which are stored in models/speakers folder.
            It is also possible to provide a full path.
        :return: the audio file as bytes
        
        """
        return self.submit_job("/text2voice", text=text, voice=voice, fine_temp=fine_temp, coarse_temp=coarse_temp, coarse_top_k=coarse_top_k, coarse_top_p=coarse_top_p, semantic_temp=semantic_temp, semantic_top_k=semantic_top_k, semantic_top_p=semantic_top_p, **kwargs)
    
    def voice2voice(self, audio_file: Union[str, MediaFile, AudioFile, Any, bytes], voice_name: Union[str, MediaFile, Any, bytes], temp: float = 0.7, **kwargs) -> APISeex:
        """
        :param audio_file: the audio file as bytes 5-20s is good length
        :param voice_name: the new of the voice to convert to; or the voice embedding. String or MediaFile.
        :param temp: generation temperature (1.0 more diverse, 0.0 more conservative)
        :return: the converted audio file as bytes
        
        """
        return self.submit_job("/voice2voice", audio_file=audio_file, voice_name=voice_name, temp=temp, **kwargs)
    
    def voice2embedding(self, audio_file: Union[str, MediaFile, AudioFile, Any, bytes], save: bool = False, voice_name: str = 'new_speaker', **kwargs) -> APISeex:
        """
        :param audio_file: the audio file as bytes 5-20s is good length
        :param voice_name: how the new voice / embedding is named
        :param save: if the embedding should be saved in the voice dir for reusage.
            Note: depending on the server settings this might not be allowed
        :return: the voice embedding as bytes
        
        """
        return self.submit_job("/voice2embedding", audio_file=audio_file, save=save, voice_name=voice_name, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = health
    __call__ = health