from dm_api_account.models import Registration, ResetPassword
from services.dm_api_account import DmApiAccount
from services.mailhog import MailhogApi
import structlog


structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


def test_post_v1_account_password():

    num = '56'

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
    reset_token = mailhog.get_token_from_last_email(reset_password=True)

    assert token != reset_token
