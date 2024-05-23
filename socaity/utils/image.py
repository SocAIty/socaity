import cv2
import numpy as np

def load_image_from_file(image_path: str) -> np.ndarray:
    """
    Load an image from a file path.
    """
    return cv2.imread(image_path)