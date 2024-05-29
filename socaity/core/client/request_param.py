class RequestParam:
    def __init__(self, name: str, val, method: str = "post"):
        self.name = name
        self.val = val
        self.method = method


class RequestParams:
    def __init__(self, get_params: dict = None, post_params: dict = None, files: dict =None):
        self.get_params = get_params
        self.post_params = post_params
        self.files = files

    def __from_dict__(self, params: dict):
        self.get_params = params.get('get_params', None)
        self.post_params = params.get('post_params', None)
        self.files = params.get('files', None)
        return self

    def __from__tuple__(self, params: tuple):
        self.get_params = params[0]
        self.post_params = params[1]
        self.files = params[2]
        return self


