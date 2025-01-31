from typing import Union, List

import media_toolkit as mt
import numpy as np

class _BaseImage2Text:
    def image2text(self, image: Union[np.array, bytes, str, mt.ImageFile], *args, **kwargs) \
            -> Union[mt.ImageFile, List[mt.ImageFile], None]:
        """
        Converts text to an image
        :param text: The text to convert to an image
        :return: The image
        """
        raise NotImplementedError("Please implement this method")

    # alias
    caption_image = image2text



# Factory method for generalized model_hosting_info calling
def image2text(
        image: Union[np.array, bytes, str, mt.ImageFile],
        model="blip", service="socaity", *args, **kwargs) -> Union[mt.VideoFile, List[mt.VideoFile], None]:
    if model == "blip":
        from .bl.hunyuan_video import HunyuanVideo
        s = HunyuanVideo(service=service)
        return s.text2video(text, *args, **kwargs)


    return None
