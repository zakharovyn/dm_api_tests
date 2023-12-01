from generic.assertions.post_v1_account import AssertionsPostV1Account
from generic.helpers.mailhog import MailhogApi
from generic.helpers.dm_db import DmDatabase
from generic.helpers.orm_db import OrmDatabase
from services.dm_api_account import Facade
from collections import namedtuple
from pathlib import Path
from vyper import v
import structlog
import pytest
import allure

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


@pytest.fixture
def mailhog():
    return MailhogApi(host=v.get('service.mailhog'))


@pytest.fixture
def facade(mailhog):
    return Facade(
        host=v.get('service.dm_api_account'),
        mailhog=mailhog
    )


connect = None


@pytest.fixture
def db():
    global connect
    if connect is None:
        connect = DmDatabase(
            user=v.get('database.dm3_5.user'),
            password=v.get('database.dm3_5.password'),
            host=v.get('database.dm3_5.host'),
            database=v.get('database.dm3_5.database')
        )
    return connect
    # connect.db.db.close()


@pytest.fixture
def assertions(db):
    return AssertionsPostV1Account(db)


@pytest.fixture
def orm():
    orm = OrmDatabase(
        user=v.get('database.dm3_5.user'),
        password=v.get('database.dm3_5.password'),
        host=v.get('database.dm3_5.host'),
        database=v.get('database.dm3_5.database')
    )
    yield orm
    orm.db.close_connection()


@allure.step('Подготовка тестового пользователя')
@pytest.fixture
def prepare_user(mailhog, facade, db):
    user = namedtuple('User', 'login, email, password')
    User = user(login=f"new_user105", email=f"new_user105@email.com", password=f"new_user105")

    db.delete_user_by_login(login=User.login)
    dataset = db.get_user_by_login(login=User.login)
    assert len(dataset) == 0

    facade.mailhog.delete_all_messages()

    return User


options = (
    'service.dm_api_account',
    'service.mailhog',
    'database.dm3_5.host'
)


@pytest.fixture(autouse=True)
def set_config(request):
    config = Path(__file__).parent.joinpath('config')
    config_name = request.config.getoption('--env')
    v.set_config_name(config_name)
    v.add_config_path(config)
    v.read_in_config()
    for option in options:
        v.set(option, request.config.getoption(f'--{option}'))


def pytest_addoption(parser):
    parser.addoption('--env', action='store', default='stg')
    for option in options:
        parser.addoption(f'--{option}', action='store', default=None)
