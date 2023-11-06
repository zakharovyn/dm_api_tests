from dm_api_account.models.request_post_v1_account_login_model import LoginCredentialsModel
from dm_api_account.models.request_post_v1_account_model import RegistrationModel
from services.dm_api_account import DmApiAccount
from services.mailhog import MailhogApi
import structlog


structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


def test_post_v1_account_login():

    mailhog = MailhogApi(host='http://5.63.153.31:5025')
    api = DmApiAccount(host='http://5.63.153.31:5051')

    json = RegistrationModel(
        login="new_user25",
        email="new_user25@email.com",
        password="new_user25"
    )
    response = api.account.post_v1_account(json=json)
    assert response.status_code == 201, f'Статус код ответа должен быть равено 201, но он равен {response.status_code}'

    token = mailhog.get_token_from_last_email()
    response = api.account.put_v1_account_token(token=token)
    assert response.status_code == 200, f'Статус код ответа должен быть равено 200, но он равен {response.status_code}'

    json = LoginCredentialsModel(
        login="new_user25",
        password="new_user25",
        rememberMe=True
    )
    response = api.login.post_v1_account_login(json=json)
    assert response.status_code == 200, f'Статус код ответа должен быть равено 200, но он равен {response.status_code}'