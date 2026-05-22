from typing import Callable

from src.main.api.foundation.endpoint import Endpoint


class HttpRequester:

    def __init__(self, request_spec: dict[str, str], response_spec: Callable, endpoint: Endpoint):
        self.request_spec = request_spec
        self.response_spec = response_spec
        self.endpoint = endpoint
