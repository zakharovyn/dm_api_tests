from db_client.db_client import DbClient
import allure


class DmDatabase:

    def __init__(self, user, password, host, database):
        self.db = DbClient(user, password, host, database)

    def get_all_users(self):
        with allure.step('Запрос списка всех пользователей'):
            query = 'select * from "public"."Users"'
            dataset = self.db.send_query(query=query)
        return dataset

    def get_user_by_login(self, login: str):
        with allure.step('Проверка наличия пользователя в бд по его логину'):
            query = f'''
            select * from "public"."Users"
            where "Login" = '{login}'
            '''
            dataset = self.db.send_query(query=query)
        return dataset

    def delete_user_by_login(self, login: str):
        with allure.step('Удаление пользователя из бд по логину'):
            query = f'''
            delete from "public"."Users" 
            where "Login" = '{login}'
            '''
            dataset = self.db.send_bulk_query(query=query)
        return dataset

    def update_activation_status(self, login: str, activation_status: str):
        with allure.step('Убновление статуса активации уз по логину пользователя'):
            query = f'''
            update "public"."Users" 
            set "Activated" = {activation_status} 
            where "Login" = '{login}'
            '''
            dataset = self.db.send_bulk_query(query=query)
        return dataset
