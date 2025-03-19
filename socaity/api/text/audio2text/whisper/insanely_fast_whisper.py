from typing import Union

from fastsdk.jobs.threaded.internal_job import InternalJob
from fastsdk.fast_sdk import fastSDK, fastJob
from media_toolkit import  AudioFile
from socaity.api.text.audio2text.audio2text import _BaseAudio2Text
from socaity.api.text.audio2text.whisper.whisper_service_client import srvc_whisper, WhisperTasks, WhisperTimeStamp


@fastSDK(api_client=srvc_whisper)
class InsanelyFastWhisper(_BaseAudio2Text):
    """
    Base implementation for SAM 2, the Segment Anything v2 model from Meta.
    """
    @fastJob
    def _whisper(self, job,
        audio: Union[str, bytes, AudioFile],
        task: str = WhisperTasks.TRANSCRIBE,
        language: str = None,
        batch_size: int = 64,
        timestamp: WhisperTimeStamp = WhisperTimeStamp.WORD,
        **kwargs
    ) -> str:
        """
        Create an image description (caption) for the input image.
        """
        tsk = task.value if isinstance(task, WhisperTasks) else task
        ts = timestamp.value if isinstance(timestamp, WhisperTimeStamp) else timestamp
        language = "None" if not language else language

        response = job.request(
            endpoint_route="/transcribe",
            audio=audio,
            task=tsk,
            language=language,
            batch_size=batch_size,
            timestamp=ts,
            **kwargs,
        )
        res = response.get_result()
        if response.error:
            raise Exception(f"Error in whisper: {response.error}")

        return res

    def transcribe(
            self,
            audio: Union[str, bytes, AudioFile],
            language: str = None,
            batch_size: int = 64,
            timestamp: WhisperTimeStamp = WhisperTimeStamp.WORD,
            *args, **kwargs
    ) -> InternalJob:
        """
        :param audio: the audio file to transcribe
        :param language: the language of the audio file. If not given it will be detected.
        :param batch_size: the batch size for the transcription. Bigger batch sizes are faster but require more memory.
        :param timestamp: the timestamp for the transcription. It can be word, sentence or paragraph.
        """
        return self._whisper(
            audio=audio,
            task=WhisperTasks.TRANSCRIBE,
            language=language, batch_size=batch_size, timestamp=timestamp, *args, **kwargs
        )

    def translate(
            self,
            audio: Union[str, bytes, AudioFile],
            batch_size: int = 64,
            timestamp: WhisperTimeStamp = WhisperTimeStamp.WORD,
            *args, **kwargs
    ) -> InternalJob:
        """ will transcribe and translate the audio to english.
        :param audio: the audio file to transcribe and translate
        :param batch_size: the batch size for the transcription. Bigger batch sizes are faster but require more memory.
        :param timestamp: the timestamp for the transcription. It can be word, sentence or paragraph.
        """
        return self._whisper(
            audio=audio,
            task=WhisperTasks.TRANSLATE,
            batch_size=batch_size,
            timestamp=timestamp, *args, **kwargs
        )
