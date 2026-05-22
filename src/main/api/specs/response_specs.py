from typing import Callable

from requests import Response
from http import HTTPStatus


class ResponseSpecs:

    @staticmethod
    def request_ok() -> Callable[[Response], None]:
        def confirm(response: Response) -> None:
            assert response.status_code == HTTPStatus.OK, response.text
        return confirm

    @staticmethod
    def request_created() -> Callable[[Response], None]:
        def confirm(response: Response) -> None:
            assert response.status_code == HTTPStatus.CREATED
        return confirm

    @staticmethod
    def request_bad() -> Callable[[Response], None]:
        def confirm(response: Response) -> None:
            assert response.status_code == HTTPStatus.BAD_REQUEST
        return confirm

    @staticmethod
    def request_not_found()  -> Callable[[Response], None]:
        def confirm(response: Response) -> None:
            assert response.status_code == HTTPStatus.NOT_FOUND
        return confirm

    @staticmethod
    def unprocessable_entity() -> Callable[[Response], None]:
        def confirm(response: Response) -> None:
            assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        return confirm