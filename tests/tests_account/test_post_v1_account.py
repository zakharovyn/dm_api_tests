from dm_api_account.model.rating import Rating
from dm_api_account.model.user_role import UserRole
from hamcrest import assert_that, has_properties
import allure


@allure.suite('Тесты на проверку метода на POST{host}/v1/account')
@allure.sub_suite('Позитивные проверки')
class TestsPostV1Account:

    @allure.title('Проверка регистрации и активации пользователя')
    def test_post_v1_account(self, facade, db, prepare_user, assertions):
        login = prepare_user.login
        email = prepare_user.email
        password = prepare_user.password

        facade.account.register_new_user(login=login, email=email, password=password)
        assertions.check_user_was_created(login=login)

        db.update_activation_status(login='new_user105', activation_status='true')
        assertions.check_user_war_activated(login=login)

        response = facade.login.login_user(login=login, password=password)

        print([UserRole.allowed_values[('value',)]['GUEST'], UserRole.allowed_values[('value',)]['PLAYER']])
        with allure.step('Проверка ответа при авторизации пользователя'):
            assert_that(response.resource, has_properties({
                "login": login,
                "roles": [UserRole.allowed_values[('value',)]['GUEST'], UserRole.allowed_values[('value',)]['PLAYER']],
                "rating": Rating(enabled=True, quality=0, quantity=0)
            }))
