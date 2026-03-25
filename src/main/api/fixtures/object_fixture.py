import logging
from typing import Any

import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_response import CreateUserResponse


def clean_users(objects: list[Any]) -> None:
    api_manager = ApiManager(objects)

    for obj in objects:
        if isinstance(obj, CreateUserResponse):
            api_manager.admin_steps.delete_user(obj.id)
            print('Очистка')
        else:
            logging.warning(f'Ошибка удаление пользователся с ID: {obj.id}')

@pytest.fixture
def created_object():
    objects: list[Any] = []
    yield objects
    clean_users(objects)