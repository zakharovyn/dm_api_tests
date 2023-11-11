from dm_api_account.models.registration_model import Registration
from services.dm_api_account import DmApiAccount
import structlog


structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


def test_post_v1_account():

    num = ''

    api = DmApiAccount(host='http://5.63.153.31:5051')

    json = Registration(
        login=f"new_user{num}",
        email=f"new_user{num}@email.com",
        password=f"new_user{num}"
    )
    api.account.post_v1_account(json=json)
