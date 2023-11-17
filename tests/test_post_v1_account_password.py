from services.dm_api_account import Facade
import structlog


structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


def test_post_v1_account_password():

    api = Facade(host='http://5.63.153.31:5051')

    num = '90'

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

    assert token != new_token
