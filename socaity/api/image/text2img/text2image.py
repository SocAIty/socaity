import media_toolkit as mt

class Text2Image:
    def text2img(self, text, *args, **kwargs) -> mt.ImageFile:
        """
        Converts text to an image
        :param text: The text to convert to an image
        :return: The image
        """
        raise NotImplementedError("Please implement this method")
