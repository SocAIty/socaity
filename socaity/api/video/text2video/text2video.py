from typing import Union, List

import media_toolkit as mt

class _BaseText2Video:
    def text2video(self, text, *args, **kwargs) -> Union[mt.VideoFile, List[mt.VideoFile], None]:
        """
        Converts text to an image
        :param text: The text to convert to an image
        :return: The image
        """
        raise NotImplementedError("Please implement this method")


# Factory method for generalized model_hosting_info calling
def text2video(text, model="hunyuan_video", service="socaity", *args, **kwargs) -> Union[mt.VideoFile, List[mt.VideoFile], None]:
    if model == "hunyuan_video":
        from .hunyuan_video.hunyuan_video import HunyuanVideo
        s = HunyuanVideo(service=service)
        return s.text2video(text, *args, **kwargs)


    return None
