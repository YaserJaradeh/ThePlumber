from hammock import Hammock


class BaseWebLinker:
    """
    Base linker class that relies on web API
    """
    def __init__(self, api_url: str):
        self.api_url = api_url
        self.client = Hammock(self.api_url)

