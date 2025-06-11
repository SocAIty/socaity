from fastsdk.fastSDK import FastSDK
from typing import Union

from media_toolkit import MediaFile


class diffbir(FastSDK):
    """
    Generated client for diffbir
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="dd56cc7b-b00a-4f56-ba78-80895bdb7a58", api_key=api_key)
    
    def predict(self, input: Union[MediaFile, str, bytes], seed: int = 231, steps: int = 50, tiled: bool = False, tile_size: int = 512, has_aligned: bool = False, tile_stride: int = 256, repeat_times: int = 1, use_guidance: bool = False, color_fix_type: str = 'wavelet', guidance_scale: float = 0.0, guidance_space: str = 'latent', guidance_repeat: int = 5, only_center_face: bool = False, guidance_time_stop: int = -1, guidance_time_start: int = 1001, background_upsampler: str = 'RealESRGAN', face_detection_model: str = 'retinaface_resnet50', upscaling_model_type: str = 'general_scenes', restoration_model_type: str = 'general_scenes', super_resolution_factor: int = 4, disable_preprocess_model: bool = False, reload_restoration_model: bool = False, background_upsampler_tile: int = 400, background_upsampler_tile_stride: int = 400, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            input: Path to the input image you want to enhance.
            
            seed: Random seed to ensure reproducibility. Setting this ensures that multiple runs with the same input produce the same output. Defaults to 231.
            
            steps: The number of enhancement iterations to perform. More steps might result in a clearer image but can also introduce artifacts. Defaults to 50.
            
            tiled: Whether to use patch-based sampling. This can be useful for very large images to enhance them in smaller chunks rather than all at once. Defaults to False.
            
            tile_size: Size of each tile (or patch) when 'tiled' option is enabled. Determines how the image is divided during patch-based enhancement. Defaults to 512.
            
            has_aligned: For 'faces' mode: Indicates if the input images are already cropped and aligned to faces. If not, the model will attempt to do this. Defaults to False.
            
            tile_stride: Distance between the start of each tile when the image is divided for patch-based enhancement. A smaller stride means more overlap between tiles. Defaults to 256.
            
            repeat_times: Number of times the enhancement process is repeated by feeding the output back as input. This can refine the result but might also introduce over-enhancement issues. Defaults to 1.
            
            use_guidance: Use latent image guidance for enhancement. This can help in achieving more accurate and contextually relevant enhancements. Defaults to False.
            
            color_fix_type: Method used for color correction post enhancement. 'wavelet' and 'adain' offer different styles of color correction, while 'none' skips this step. Defaults to 'wavelet'.
            
            guidance_scale: For 'general_scenes': Scale factor for the guidance mechanism. Adjusts the influence of guidance on the enhancement process. Defaults to 0.0.
            
            guidance_space: For 'general_scenes': Determines in which space (RGB or latent) the guidance operates. 'latent' can often provide more subtle and context-aware enhancements. Defaults to 'latent'.
            
            guidance_repeat: For 'general_scenes': Number of times the guidance process is repeated during enhancement. Defaults to 5.
            
            only_center_face: For 'faces' mode: If multiple faces are detected, only enhance the center-most face in the image. Defaults to False.
            
            guidance_time_stop: For 'general_scenes': Specifies when (at which step) the guidance mechanism stops influencing the enhancement. Defaults to -1.
            
            guidance_time_start: For 'general_scenes': Specifies when (at which step) the guidance mechanism starts influencing the enhancement. Defaults to 1001.
            
            background_upsampler: For 'faces' mode: Model used to upscale the background in images where the primary subject is a face. Defaults to 'RealESRGAN'.
            
            face_detection_model: For 'faces' mode: Model used for detecting faces in the image. Choose based on accuracy and speed preferences. Defaults to 'retinaface_resnet50'.
            
            upscaling_model_type: Choose the type of model best suited for the primary content of the image: 'faces' for portraits and 'general_scenes' for everything else. Defaults to 'general_scenes'.
            
            restoration_model_type: Select the restoration model that aligns with the content of your image. This model is responsible for image restoration which removes degradations. Defaults to 'general_scenes'.
            
            super_resolution_factor: Factor by which the input image resolution should be increased. For instance, a factor of 4 will make the resolution 4 times greater in both height and width. Defaults to 4.
            
            disable_preprocess_model: Disables the initial preprocessing step using SwinIR. Turn this off if your input image is already of high quality and doesn't require restoration. Defaults to False.
            
            reload_restoration_model: Reload the image restoration model (SwinIR) if set to True. This can be useful if you've updated or changed the underlying SwinIR model. Defaults to False.
            
            background_upsampler_tile: For 'faces' mode: Size of each tile used by the background upsampler when dividing the image into patches. Defaults to 400.
            
            background_upsampler_tile_stride: For 'faces' mode: Distance between the start of each tile when the background is divided for upscaling. A smaller stride means more overlap between tiles. Defaults to 400.
            
        """
        return self.submit_job("/predict", input=input, seed=seed, steps=steps, tiled=tiled, tile_size=tile_size, has_aligned=has_aligned, tile_stride=tile_stride, repeat_times=repeat_times, use_guidance=use_guidance, color_fix_type=color_fix_type, guidance_scale=guidance_scale, guidance_space=guidance_space, guidance_repeat=guidance_repeat, only_center_face=only_center_face, guidance_time_stop=guidance_time_stop, guidance_time_start=guidance_time_start, background_upsampler=background_upsampler, face_detection_model=face_detection_model, upscaling_model_type=upscaling_model_type, restoration_model_type=restoration_model_type, super_resolution_factor=super_resolution_factor, disable_preprocess_model=disable_preprocess_model, reload_restoration_model=reload_restoration_model, background_upsampler_tile=background_upsampler_tile, background_upsampler_tile_stride=background_upsampler_tile_stride, **kwargs)
     