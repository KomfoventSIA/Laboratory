class StandException(Exception):
    def __init__(self, exception_name):
        self.exception_name: str = exception_name

    def get_exception_name(self):
        return self.exception_name
