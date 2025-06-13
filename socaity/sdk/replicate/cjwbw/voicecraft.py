from fastsdk.fastSDK import FastSDK
from typing import Union, Optional

from media_toolkit import MediaFile


class voicecraft(FastSDK):
    """
    Generated client for cjwbw/voicecraft
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="93620bcc-7660-48a9-8c9e-0e59df84af65", api_key=api_key)
    
    def predict(self, orig_audio: Union[MediaFile, str, bytes], target_transcript: str, task: str = 'zero-shot text-to-speech', top_p: float = 0.9, kvcache: int = 1, cut_off_sec: float = 3.01, left_margin: float = 0.08, temperature: float = 1.0, right_margin: float = 0.08, whisperx_model: str = 'base.en', orig_transcript: str = '', stop_repetition: int = 3, voicecraft_model: str = 'giga330M_TTSEnhanced.pth', sample_batch_size: int = 4, seed: Optional[int] = None, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            orig_audio: Original audio file
            
            target_transcript: Transcript of the target audio file
            
            task: Choose a task Defaults to 'zero-shot text-to-speech'.
            
            top_p: Default value for TTS is 0.9, and 0.8 for speech editing Defaults to 0.9.
            
            kvcache: Set to 0 to use less VRAM, but with slower inference Defaults to 1.
            
            cut_off_sec: Only used for for zero-shot text-to-speech task. The first seconds of the original audio that are used for zero-shot text-to-speech. 3 sec of reference is generally enough for high quality voice cloning, but longer is generally better, try e.g. 3~6 sec Defaults to 3.01.
            
            left_margin: Margin to the left of the editing segment Defaults to 0.08.
            
            temperature: Adjusts randomness of outputs, greater than 1 is random and 0 is deterministic. Do not recommend to change Defaults to 1.0.
            
            right_margin: Margin to the right of the editing segment Defaults to 0.08.
            
            whisperx_model: If orig_transcript is not provided above, choose a WhisperX model for generating the transcript. Inaccurate transcription may lead to error TTS or speech editing. You can modify the generated transcript and provide it directly to orig_transcript above Defaults to 'base.en'.
            
            orig_transcript: Optionally provide the transcript of the input audio. Leave it blank to use the WhisperX model below to generate the transcript. Inaccurate transcription may lead to error TTS or speech editing Defaults to ''.
            
            stop_repetition: Default value for TTS is 3, and -1 for speech editing. -1 means do not adjust prob of silence tokens. if there are long silence or unnaturally stretched words, increase sample_batch_size to 2, 3 or even 4 Defaults to 3.
            
            voicecraft_model: Choose a model Defaults to 'giga330M_TTSEnhanced.pth'.
            
            sample_batch_size: Default value for TTS is 4, and 1 for speech editing. The higher the number, the faster the output will be. Under the hood, the model will generate this many samples and choose the shortest one Defaults to 4.
            
            seed: Random seed. Leave blank to randomize the seed Optional.
            
        """
        return self.submit_job("/predictions", orig_audio=orig_audio, target_transcript=target_transcript, task=task, top_p=top_p, kvcache=kvcache, cut_off_sec=cut_off_sec, left_margin=left_margin, temperature=temperature, right_margin=right_margin, whisperx_model=whisperx_model, orig_transcript=orig_transcript, stop_repetition=stop_repetition, voicecraft_model=voicecraft_model, sample_batch_size=sample_batch_size, seed=seed, **kwargs)
     