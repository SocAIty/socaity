from fastsdk import FastSDK, APISeex
from typing import Dict, List, Any, Union

from media_toolkit import ImageFile, MediaFile, VideoFile


class face2face(FastSDK):
    """
    Swap faces from images and videos. Create face embeddings.
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="0d69b27a-f893-4582-b3e8-a18c1f588e90", api_key=api_key)
    
    def swap(self, faces: Union[MediaFile, List[Any], Dict[str, Any], str, Any, bytes], media: Union[str, MediaFile, ImageFile, Any, bytes], enhance_face_model: str = 'gpen_bfr_512', **kwargs) -> APISeex:
        """
        Swap faces in an image or video.
        
        Args:
            faces: The face(s) to swap to. Can be:
                - str: Name of a reference face
                - dict: Swap pairs with structure {source_face_name: target_face_name}
                - list: List of face names or Face embeddings
                - MediaFile: Single face embedding file
                - MediaList: Multiple face embedding files
            media: The image or video to swap faces in
            enhance_face_model: Face enhancement model to use. Defaults to 'gpen_bfr_512'
        
        Returns:
            Union[ImageFile, VideoFile]: The resulting media with swapped faces
        
        Raises:
            ValueError: If no faces are provided or media type is unsupported
        
        """
        return self.submit_job("/swap", faces=faces, media=media, enhance_face_model=enhance_face_model, **kwargs)
    
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
    
    def add_face(self, image: Union[str, MediaFile, ImageFile, Any, bytes], face_name: Union[str, List[Any]], save: bool = False, **kwargs) -> APISeex:
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
    
    def swap_video(self, faces: Union[MediaFile, List[Any], Dict[str, Any], str, Any, bytes], target_video: Union[str, MediaFile, VideoFile, Any, bytes], include_audio: bool = True, enhance_face_model: str = 'gpen_bfr_512', **kwargs) -> APISeex:
        """
        Swap faces in a video file.
        
        Args:
            job_progress: Progress tracker for the job
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
    
    def swap_img_to_img(self, source_img: Union[str, MediaFile, ImageFile, Any, bytes], target_img: Union[str, MediaFile, ImageFile, Any, bytes], enhance_face_model: str = 'gpen_bfr_512', **kwargs) -> APISeex:
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