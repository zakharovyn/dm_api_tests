from dm_api_account.models.request_post_v1_account_model import RegistrationModel
from dm_api_account.models.request_put_v1_account_email_model import ChangeEmailModel
from services.dm_api_account import DmApiAccount
from services.mailhog import MailhogApi
import structlog


structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


def test_put_v1_account_email():

    mailhog = MailhogApi(host='http://5.63.153.31:5025')
    api = DmApiAccount(host='http://5.63.153.31:5051')

    json = RegistrationModel(
        login="new_user26",
        email="new_user26@email.com",
        password="new_user26"
    )
    response = api.account.post_v1_account(json=json)
    assert response.status_code == 201, f'Статус код ответа должен быть равено 201, но он равен {response.status_code}'

    token = mailhog.get_token_from_last_email()
    response = api.account.put_v1_account_token(token=token)
    assert response.status_code == 200, f'Статус код ответа должен быть равено 200, но он равен {response.status_code}'

    json = ChangeEmailModel(
        login="new_user26",
        password="new_user26",
        email="new_new_user26@email.com"
    )
    response = api.account.put_v1_account_email(json=json)
    assert response.status_code == 200, f'Статус код ответа должен быть равено 200, но он равен {response.status_code}'
