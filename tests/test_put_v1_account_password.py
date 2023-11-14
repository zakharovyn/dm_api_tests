from dm_api_account.models.user_envelope_model import UserRole, Rating
from hamcrest import assert_that, has_properties
from services.dm_api_account import Facade
import structlog


structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


def test_put_v1_account_password():

    api = Facade(host='http://5.63.153.31:5051')

    num = '85'

    login = f"new_user{num}"
    email = f"new_user{num}@email.com"
    password = f"new_user{num}"

    api.account.register_new_user(
        login=login,
        email=email,
        password=password
    )

    api.account.activate_registered_user(login=login)

    token = api.login.get_auth_token(
        login=login,
        password=password
    )
    api.account.set_headers(headers=token)

    api.account.reset_registered_user_password(
        login=login,
        email=email
    )

    new_token = api.mailhog.get_token_by_login(
        login=login,
        reset_password=True
    )

    new_password = f"very_new_user{num}"
    response = api.account.change_registered_user_password(
        login=login,
        token=new_token,
        old_password=password,
        new_password=new_password
    )

    assert_that(response.resource, has_properties({
        "login": login,
        "roles": [UserRole.guest, UserRole.player],
        "rating": Rating(enabled=True, quality=0, quantity=0)
    }))
