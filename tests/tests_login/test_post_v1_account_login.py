from dm_api_account.models.user_envelope_model import Rating, UserRole
from hamcrest import assert_that, has_properties


def test_post_v1_account_login(facade, orm, prepare_user, assertions):
    login = prepare_user.login
    email = prepare_user.email
    password = prepare_user.password

    facade.account.register_new_user(login=login, email=email, password=password)
    assertions.check_user_was_created(login=login)

    orm.update_activation_status(login=login, activation_status=True)
    assertions.check_user_war_activated(login=login)

    response = facade.login.login_user(login=login, password=password, need_json=False)

    assert_that(response.resource, has_properties({
        "login": login,
        "roles": [UserRole.guest, UserRole.player],
        "rating": Rating(enabled=True, quality=0, quantity=0)
    }))
