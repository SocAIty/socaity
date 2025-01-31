from typing import Union

from fastsdk.jobs.threaded.internal_job import InternalJob
from fastsdk.fast_sdk import fastSDK, fastJob
from media_toolkit import ImageFile
from .sam2_service_client import srvc_sam2
from ..i_image_segmentation import _BaseSegmentation


@fastSDK(service_client=srvc_sam2)
class Sam2(_BaseSegmentation):
    """
    Base implementation for SAM 2, the Segment Anything v2 model from Meta.
    """
    @fastJob
    def _segment(self, job,
                 image: Union[str, bytes, ImageFile],
                 points_per_side: int = 32,
                 pred_iou_thresh: float = 0.88,
                 stability_score_thresh: float = 0.95,
                 use_m2m: bool = True,
                 **kwargs) -> dict:
        """
        Perform image segmentation using SAM 2.
        :param image: URL or path to the input image.
        :param points_per_side: Number of points per side for segmentation.
        :param pred_iou_thresh: Prediction IoU threshold.
        :param stability_score_thresh: Stability score threshold.
        :param use_m2m: Whether to enable model-to-model interaction.
        :return: Segmentation results as a dictionary.
        """
        response = job.request(
            endpoint_route="/segment",
            image=image,
            points_per_side=points_per_side,
            pred_iou_thresh=pred_iou_thresh,
            stability_score_thresh=stability_score_thresh,
            use_m2m=use_m2m,
            **kwargs,
        )
        res = response.get_result()
        if response.error:
            raise Exception(f"Error in segmentation: {response.error}")

        result = {}
        combined_mask = res.get("combined_mask", None)
        individual_masks = res.get("individual_masks", None)
        if combined_mask:
            result["combined_mask"] = ImageFile().from_any(combined_mask)
        if individual_masks:
            result["individual_masks"] = [ImageFile().from_any(mask) for mask in individual_masks]

        return result

    def segment(self,
        image: Union[str, bytes, ImageFile],
        points_per_side: int = 32,
        pred_iou_thresh: float = 0.88,
        stability_score_thresh: float = 0.95,
        use_m2m: bool = True,
        *args, **kwargs) -> InternalJob:
        """
        Perform image segmentation using SAM 2.
        :param image: URL or path to the input image.
        """
        return self._segment(image=image, **kwargs)

