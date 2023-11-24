from dm_api_account.models.user_envelope_model import UserRole, Rating
from hamcrest import assert_that, has_properties, has_entries


def test_post_v1_account(facade, db, prepare_user):
    login = prepare_user.login
    email = prepare_user.email
    password = prepare_user.password

    facade.account.register_new_user(
        login=login,
        email=email,
        password=password
    )

    dataset = db.get_user_by_login(login=login)
    for row in dataset:
        assert_that(row, has_entries(
            {
                'Login': login,
                'Activated': False
            }
        ))

    db.update_activation_status(login='new_user105', activation_status='true')

    dataset = db.get_user_by_login(login=login)
    for row in dataset:
        assert_that(row, has_entries(
            {
                'Activated': True
            }
        ))

    response = facade.login.login_user(
        login=login,
        password=password,
        need_json=False
    )

    assert_that(response.resource, has_properties({
        "login": login,
        "roles": [UserRole.guest, UserRole.player],
        "rating": Rating(enabled=True, quality=0, quantity=0)
    }))
