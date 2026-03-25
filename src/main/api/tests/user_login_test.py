from mimesis import Person

from src.main.api.models.login_user_request import LoginUserRequest

person = Person()

class TestUserLogin:
    def test_admin_login(self, api_manager):
        login_user_request = LoginUserRequest(username='admin', password='123456')

        response = api_manager.admin_steps.login_user(login_user_request)

        assert login_user_request.username == response.user.username
        assert response.user.role == 'ROLE_ADMIN'

    def test_user_login(self, api_manager, create_user):
        login_user_response = api_manager.admin_steps.login_user(create_user)

        assert create_user.username == login_user_response.user.username
        assert login_user_response.user.role == 'ROLE_USER'


