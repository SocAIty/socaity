from typing import Tuple
from io import BytesIO

import librosa
import soundfile as sf
import numpy as np

def audio_from_bytes(audio_bytes: bytes, save_file_path: str = None) -> Tuple[np.ndarray, float]:
    """ returns audio array from bytes """
    audio_file, sr = librosa.load(BytesIO(audio_bytes))
    if save_file_path is not None:
        # save to file
        sf.write(save_file_path, audio_file, sr)

    return audio_file, sr