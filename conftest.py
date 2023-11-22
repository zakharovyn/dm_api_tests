from generic.helpers.mailhog import MailhogApi
from generic.helpers.dm_db import DmDatabase
from generic.helpers.orm_db import OrmDatabase
from services.dm_api_account import Facade
from collections import namedtuple
import structlog
import pytest

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


@pytest.fixture
def mailhog():
    return MailhogApi(host='http://5.63.153.31:5025')


@pytest.fixture
def facade(mailhog):
    return Facade(host='http://5.63.153.31:5051', mailhog=mailhog)


@pytest.fixture
def db():
    db = DmDatabase(user='postgres', password='admin', host='5.63.153.31', database='dm3.5')
    return db


@pytest.fixture
def orm():
    orm = OrmDatabase(user='postgres', password='admin', host='5.63.153.31', database='dm3.5')
    yield orm
    orm.db.close_connection()


@pytest.fixture
def prepare_user(mailhog, facade, db):
    user = namedtuple('User', 'login, email, password')
    User = user(login=f"new_user105", email=f"new_user105@email.com", password=f"new_user105")

    db.delete_user_by_login(login=User.login)
    dataset = db.get_user_by_login(login=User.login)
    assert len(dataset) == 0

    facade.mailhog.delete_all_messages()

    return User
