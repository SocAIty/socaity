import re
import unicodedata


def encode_path_safe(filename: str, allow_unicode=False):
    """
    Makes a string path safe by removing / replacing not by the os allowed patterns.
    This converts:
    spaces 2 dashes, repeated dashes 2 single dashes, remove non alphanumerics, underscores, or hyphen, string 2 lowercase
    strip
    """
    filename = str(filename)
    if allow_unicode:
        filename = unicodedata.normalize('NFKC', filename)
    else:
        filename = unicodedata.normalize('NFKD', filename).encode('ascii', 'ignore').decode('ascii')
    filename = re.sub(r'[^\w\s-]', '', filename.lower())
    return re.sub(r'[-\s]+', '-', filename).strip('-_')


def get_function_parameters_as_dict(func, named_locals: dict, kwargs: dict = None):
    """
    Get the parameters of a function as a dict
    :param func: the function to get the parameters from
    :param named_locals: the local variables (args) of the function you can get them in your function with locals()
    :param kwargs: the named parameters of the function usually you get them with **kwargs
    :return: a dict with the parameters as key and the value as value
    """
    kwargs = {} if kwargs is None else kwargs  # makes it easier to process further

    # filter locals and kwargs with excludes
    excludes = ["self", "cls", "args", "kwargs"]
    named_locals = {k: v for k, v in named_locals.items() if k not in excludes}
    kwargs = {k: v for k, v in kwargs.items() if k not in excludes}
    # get the parameters of the function
    named_locals = {k: v for k, v in named_locals.items() if k in func.__code__.co_varnames}
    # update locls with kwargs
    named_locals.update(kwargs)
    return named_locals