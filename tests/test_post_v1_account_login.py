from dm_api_account.models.login_credentials_model import LoginCredentials
from dm_api_account.models.user_envelope_model import UserRole, Rating
from dm_api_account.models.registration_model import Registration
from services.dm_api_account import DmApiAccount
from hamcrest import assert_that, has_properties
from services.mailhog import MailhogApi
import structlog


structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


def test_post_v1_account_login():

    num = '57'

    mailhog = MailhogApi(host='http://5.63.153.31:5025')
    api = DmApiAccount(host='http://5.63.153.31:5051')

    json = Registration(
        login=f"new_user{num}",
        email=f"new_user{num}@email.com",
        password=f"new_user{num}"
    )
    api.account.post_v1_account(json=json)

    token = mailhog.get_token_from_last_email()
    api.account.put_v1_account_token(token=token)

    json = LoginCredentials(
        login=f"new_user{num}",
        password=f"new_user{num}",
        rememberMe=True
    )
    response = api.login.post_v1_account_login(json=json)

    assert_that(response.resource, has_properties({
        "login": f"new_user{num}",
        "roles": [UserRole.guest, UserRole.player],
        "rating": Rating(enabled=True, quality=0, quantity=0)
    }))
