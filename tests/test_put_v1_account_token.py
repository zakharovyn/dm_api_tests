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


def test_put_v1_account_token():

    orm = OrmDatabase(user='postgres', password='admin', host='5.63.153.31', database='dm3.5')
    api = Facade(host='http://5.63.153.31:5051')

    num = '93'

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

    response = api.account.activate_registered_user(login=login)

    assert_that(response.resource, has_properties({
        "login": login,
        "roles": [UserRole.guest, UserRole.player],
        "rating": Rating(enabled=True, quality=0, quantity=0)
    }))

    orm.db.close_connection()
