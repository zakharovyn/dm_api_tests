from dm_api_account.models.user_envelope_model import Rating, UserRole
from hamcrest import assert_that, has_properties
from services.dm_api_account import Facade
import structlog


structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


def test_post_v1_account_login():

    api = Facade(host='http://5.63.153.31:5051')

    num = '99'

    login = f"new_user{num}"
    email = f"new_user{num}@email.com"
    password = f"new_user{num}"

    api.account.register_new_user(
        login=login,
        email=email,
        password=password
    )

    api.account.activate_registered_user(login=login)

    response = api.login.login_user(login=login, password=password, need_json=False)

    assert_that(response.resource, has_properties({
        "login": login,
        "roles": [UserRole.guest, UserRole.player],
        "rating": Rating(enabled=True, quality=0, quantity=0)
    }))
