from sqlalchemy import select, delete, update
from generic.helpers.orm_models import User
from orm_client.orm_client import OrmClient
from typing import List
import allure


class OrmDatabase:

    def __init__(self, user, password, host, database):
        self.db = OrmClient(user, password, host, database)

    def get_all_users(self):
        with allure.step('Запрос списка всех пользователей'):
            query = select(User)
            dataset = self.db.send_query(query)
        return dataset

    def get_user_by_login(self, login: str) -> List[User]:
        with allure.step('Проверка наличия пользователя в бд по его логину'):
            query = select(User).where(
                User.Login == login
            )
            dataset = self.db.send_query(query)
        return dataset

    def delete_user_by_login(self, login: str):
        with allure.step('Удаление пользователя из бд по логину'):
            query = delete(User).where(
                User.Login == login
            )
            dataset = self.db.send_bulk_query(query=query)
        return dataset

    def update_activation_status(self, login: str, activation_status: bool):
        with allure.step('Убновление статуса активации уз по логину пользователя'):
            query = update(User).where(
                User.Login == login
            ).values(Activated=activation_status)
            dataset = self.db.send_bulk_query(query=query)
        return dataset
