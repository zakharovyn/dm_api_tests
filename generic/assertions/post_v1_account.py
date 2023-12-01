from hamcrest import assert_that, has_entries
from generic.helpers.dm_db import DmDatabase
import allure


class AssertionsPostV1Account:

    def __init__(self, db: DmDatabase):
        self.db = db

    def check_user_was_created(self, login: str):
        with allure.step('Проверка, что пользователь был создан'):
            dataset = self.db.get_user_by_login(login=login)
            for row in dataset:
                assert_that(row, has_entries(
                    {
                        'Login': login,
                        'Activated': False
                    }
                ))

    def check_user_war_activated(self, login: str):
        with allure.step('Проверка, что пользователь был активирован'):
            dataset = self.db.get_user_by_login(login=login)
            for row in dataset:
                assert_that(row, has_entries(
                    {
                        'Activated': True
                    }
                ))
