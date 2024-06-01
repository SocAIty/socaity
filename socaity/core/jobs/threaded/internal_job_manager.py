from singleton_decorator import singleton


@singleton
class InternalJobManager:
    def __init__(self):
        self.queue = []

    def submit(self, func: callable):
        a =1