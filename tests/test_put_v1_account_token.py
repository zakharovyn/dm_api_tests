from dm_api_account.models.user_envelope_model import UserRole, Rating
from hamcrest import assert_that, has_properties


def test_put_v1_account_token(facade, orm, prepare_user):
    login = prepare_user.login
    email = prepare_user.email
    password = prepare_user.password

    orm.delete_user_by_login(login=login)

    dataset = orm.get_user_by_login(login=login)
    assert len(dataset) == 0

    facade.account.register_new_user(
        login=login,
        email=email,
        password=password
    )

    response = facade.account.activate_registered_user(login=login)

    assert_that(response.resource, has_properties({
        "login": login,
        "roles": [UserRole.guest, UserRole.player],
        "rating": Rating(enabled=True, quality=0, quantity=0)
    }))
