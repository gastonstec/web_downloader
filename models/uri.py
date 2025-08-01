
class URI:
    def __init__(self, scheme: str, host: str, path: str):
        self.scheme: str = scheme
        self.host: str = host
        self.path: str = path

    def __str__(self):
        return f"{self.scheme}://{self.host}{self.path}"