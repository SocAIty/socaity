from fastsdk import FastClient, APISeex
from typing import Dict, Literal, Union, Any, List

from media_toolkit import ImageFile, VideoFile, MediaFile


class face2face(FastClient):
    """
    Swap faces from images and videos. Create face embeddings.
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="0d69b27a-f893-4582-b3e8-a18c1f588e90", api_key=api_key)
    
    def swap(self, faces: Union[List[str], Dict[str, Any], List[bytes], List[MediaFile]], media: Union[List[bytes], List[MediaFile], List[str]], enhance_face_model: Literal["", "gpen_bfr_512", "gpen_bfr_1024", "gpen_bfr_2048", "gfpgan_1.4"] = 'gpen_bfr_512', **kwargs) -> APISeex:
        """
        Swap faces in an image or video.
        
        Args:
            faces: The face(s) to swap to. Can be:
                - str: Name of a reference face
                - dict: Swap pairs with structure {source_face_name: target_face_name}
                - list: List of face names or Face embeddings
                - ImageFile: Use face detection to create a face embedding from the image.
                - MediaFile: Single face embedding file
                - MediaList: Multiple face embeddings
            media: The image(s) or video(s) to swap faces in
            enhance_face_model: Face enhancement model to use. Defaults to 'gpen_bfr_512'
        
        Returns:
            Union[ImageFile, VideoFile]: The resulting media with swapped faces
        
        Raises:
            ValueError: If no faces are provided or media type is unsupported
        
        """
        return self.submit_job("/swap", faces=faces, media=media, enhance_face_model=enhance_face_model, **kwargs)
    
    def add_face(self, image: Union[bytes, ImageFile, str], face_name: Union[str, List[str]], save: bool = False, **kwargs) -> APISeex:
        """
        Add one or multiple reference face(s) to the face swapper.
        
        Args:
            face_name: Name(s) for the reference face(s).
                - If a single string, creates one face embedding
                - If a list of strings, creates embeddings for each face from left to right in the image
            image: The image from which to extract the face(s).
                - ImageFile: Standard image file
            save: Whether to save the face embeddings to disk.
                Note: This is controlled by ALLOW_EMBEDDING_SAVE_ON_SERVER setting
        
        Returns:
            Union[MediaFile, MediaDict]:
                - For single face: MediaFile containing the face embedding
                - For multiple faces: MediaDict mapping face names to their embeddings
        
        Raises:
            ValueError: If no face name is provided or no faces are detected in the image
        
        """
        return self.submit_job("/add-face", image=image, face_name=face_name, save=save, **kwargs)
    
    def swap_video(self, faces: Union[List[str], Dict[str, Any], List[bytes], List[MediaFile]], target_video: Union[bytes, VideoFile, str], include_audio: bool = True, enhance_face_model: Literal["", "gpen_bfr_512", "gpen_bfr_1024", "gpen_bfr_2048", "gfpgan_1.4"] = 'gpen_bfr_512', **kwargs) -> APISeex:
        """
        Swap faces in a video file.
        
        Args:
            face_name: The face(s) to swap to. Can be:
                - str: Name of a reference face
                - list: List of face names or Face objects
                - MediaFile: Single face embedding file
                - MediaList: Multiple face embedding files
            target_video: The video to swap faces in
            include_audio: Whether to include audio in the output video
            enhance_face_model: Face enhancement model to use. Defaults to 'gpen_bfr_512'
        
        Returns:
            VideoFile: The resulting video with swapped faces
        
        Raises:
            ValueError: If no faces are provided or video cannot be processed
        
        """
        return self.submit_job("/swap-video", faces=faces, target_video=target_video, include_audio=include_audio, enhance_face_model=enhance_face_model, **kwargs)
    
    def enhance_face(self, face_image: Union[bytes, ImageFile, str, MediaFile], enhance_face_model: Literal["", "gpen_bfr_512", "gpen_bfr_1024", "gpen_bfr_2048", "gfpgan_1.4"] = 'gpen_bfr_512', **kwargs) -> APISeex:
        """
        Enhance a face image.
        
        
        Args:
            face_image: No description available.
            
            enhance_face_model: No description available. Defaults to 'gpen_bfr_512'.
            
        """
        return self.submit_job("/enhance-face", face_image=face_image, enhance_face_model=enhance_face_model, **kwargs)
    
    def swap_img_to_img(self, source_img: Union[bytes, ImageFile, str], target_img: Union[bytes, ImageFile, str], enhance_face_model: Literal["", "gpen_bfr_512", "gpen_bfr_1024", "gpen_bfr_2048", "gfpgan_1.4"] = 'gpen_bfr_512', **kwargs) -> APISeex:
        """
        Swap faces between two images.
        
        Args:
            source_img: Source image containing the face(s) to swap from
            target_img: Target image containing the face(s) to swap to
            enhance_face_model: Face enhancement model to use. Defaults to 'gpen_bfr_512'
        
        Returns:
            ImageFile: The resulting image with swapped faces
        
        """
        return self.submit_job("/swap-img-to-img", source_img=source_img, target_img=target_img, enhance_face_model=enhance_face_model, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = swap
    __call__ = swap
