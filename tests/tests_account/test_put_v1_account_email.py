from apis.dm_api_account.models.user_envelope_model import UserRole, Rating
from hamcrest import assert_that, has_properties


def test_put_v1_account_email(facade, orm, prepare_user, assertions):
    login = prepare_user.login
    email = prepare_user.email
    password = prepare_user.password

    facade.account.register_new_user(login=login, email=email, password=password)
    assertions.check_user_was_created(login=login)
    orm.update_activation_status(login=login, activation_status=True)
    assertions.check_user_war_activated(login=login)

    token = facade.login.get_auth_token(login=login, password=password)
    facade.account.set_headers(headers=token)

    new_email = f"very_new_user107@email.com"
    response = facade.account.change_registered_user_email(login=login, password=password, email=new_email)

    assert_that(response.resource, has_properties({
        "login": login,
        "roles": [UserRole.guest, UserRole.player],
        "rating": Rating(enabled=True, quality=0, quantity=0)
    }))
