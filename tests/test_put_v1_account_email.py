from dm_api_account.models.user_envelope_model import UserRole, Rating
from hamcrest import assert_that, has_properties
from generic.helpers.orm_db import OrmDatabase
from services.dm_api_account import Facade
import structlog


structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


def test_put_v1_account_email():

    orm = OrmDatabase(user='postgres', password='admin', host='5.63.153.31', database='dm3.5')
    api = Facade(host='http://5.63.153.31:5051')

    num = '91'

    login = f"new_user{num}"
    email = f"new_user{num}@email.com"
    password = f"new_user{num}"

    orm.delete_user_by_login(login=login)

    dataset = orm.get_user_by_login(login=login)
    assert len(dataset) == 0

    api.account.register_new_user(
        login=login,
        email=email,
        password=password
    )

    dataset = orm.get_user_by_login(login=login)
    for row in dataset:
        assert row.Login == login
        assert row.Activated is False

    orm.update_activation_status(login=login, activation_status=True)

    dataset = orm.get_user_by_login(login=login)
    for row in dataset:
        assert row.Activated is True

    token = api.login.get_auth_token(
        login=login,
        password=password
    )

    api.account.set_headers(headers=token)

    new_email = f"very_new_user{num}@email.com"
    response = api.account.change_registered_user_email(
        login=login,
        password=password,
        email=new_email
    )

    assert_that(response.resource, has_properties({
        "login": login,
        "roles": [UserRole.guest, UserRole.player],
        "rating": Rating(enabled=True, quality=0, quantity=0)
    }))
