from dm_api_account.models import Registration, ChangePassword, ResetPassword
from dm_api_account.models.user_envelope_model import UserRole, Rating
from services.dm_api_account import DmApiAccount
from hamcrest import assert_that, has_properties
from services.mailhog import MailhogApi
import structlog


structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


def test_put_v1_account_password():

    num = '54'

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

    reset_password_json = ResetPassword(
        login=f"new_user{num}",
        email=f"new_user{num}@email.com"
    )
    api.account.post_v1_account_password(json=reset_password_json, status_code=200)
    token = mailhog.get_token_from_last_email(reset_password=True)

    change_password_json = ChangePassword(
        login=f"new_user{num}",
        token=token,
        oldPassword=f"new_user{num}",
        newPassword="new_user47"
    )

    response = api.account.put_v1_account_password(json=change_password_json)

    assert_that(response.resource, has_properties({
        "login": f"new_user{num}",
        "roles": [UserRole.guest, UserRole.player],
        "rating": Rating(enabled=True, quality=0, quantity=0)
    }))



