from dm_api_account.models.user_envelope_model import UserRole, Rating
from hamcrest import assert_that, has_properties
from generic.helpers.dm_db import DmDatabase
from services.dm_api_account import Facade
import structlog


structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


def test_post_v1_account():

    api = Facade(host='http://5.63.153.31:5051')
    db = DmDatabase(user='postgres', password='admin', host='5.63.153.31', database='dm3.5')

    num = '106'

    login = f"new_user{num}"
    email = f"new_user{num}@email.com"
    password = f"new_user{num}"

    db.delete_user_by_login(login=login)
    dataset = db.get_user_by_login(login=login)
    assert len(dataset) == 0

    api.mailhog.delete_all_messages()

    api.account.register_new_user(
        login=login,
        email=email,
        password=password
    )

    dataset = db.get_user_by_login(login=login)
    for row in dataset:
        assert row['Login'] == login, f'User {login} not registered'
        assert row['Activated'] is False, f'User {login} was activated'

    db.update_activation_status(login='new_user106', activation_status='true')

    dataset = db.get_user_by_login(login=login)
    for row in dataset:
        assert row['Activated'] is True, f'User {login} not activated'

    response = api.login.login_user(
        login=login,
        password=password,
        need_json=False
    )

    assert_that(response.resource, has_properties({
        "login": login,
        "roles": [UserRole.guest, UserRole.player],
        "rating": Rating(enabled=True, quality=0, quantity=0)
    }))
