from hammock import Hammock


class BaseWebLinker:
    """
    Base linker class that relies on web API
    """
    def __init__(self, **kwargs):
        if 'api_url' not in kwargs:
            raise ValueError('api_url parameter should be passed to any Web Linker component')
        self.api_url = kwargs['api_url']
        self.client = Hammock(self.api_url)

