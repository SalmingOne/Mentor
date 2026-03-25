import pytest

from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest
from mimesis import Person
from src.main.api.db.crud.user_crud import UserCrudDb as User

person = Person()


class TestCreateUser:
    @pytest.mark.parametrize(
        'create_user_request', [RandomModelGenerator.generate(CreateUserRequest)]
    )
    def test_user_creation_valid(self, api_manager, create_user_request, db_session):
        response = api_manager.admin_steps.create_user(create_user_request)

        assert create_user_request.username == response.username
        assert create_user_request.role == response.role
        user_from_db = User.get_user_by_username(db_session, create_user_request.username)
        assert user_from_db.username == create_user_request.username, "Пользователя нет в Базе Данных"

    @pytest.mark.parametrize(
        'username, password',
        [
            ('абв', 'Password1.'),
            ('ab', 'Password1.'),
            ('qwertyuiopasdfgh', 'Password1.'),
            ('qwer!', 'Password1.'),
            ('qwerty', 'Passwordи1.'),
            ('qwerty', 'Pasrd1.'),
            ('qwerty', 'password1.'),
            ('qwerty', 'PASSWORD1.'),
            ('qwerty', 'Password1'),
            ('qwerty', 'Password.'),
        ])
    def test_user_creation_invalid(self, username, password, api_manager, db_session):
        create_user_request = CreateUserRequest(username=username, password=password, role='ROLE_USER')
        api_manager.admin_steps.create_invalid_user(create_user_request)

        assert User.get_user_by_username(db_session, username) is None, 'Пользователь создан, ошибка'

