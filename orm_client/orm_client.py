from sqlalchemy import create_engine
import structlog
import allure
import uuid


class OrmClient:

    def __init__(self, user, password, host, database, isolation_level='AUTOCOMMIT'):
        connection_string = f"postgresql://{user}:{password}@{host}/{database}"
        self.engine = create_engine(connection_string, isolation_level=isolation_level)
        self.db = self.engine.connect()
        self.log = structlog.get_logger(self.__class__.__name__).bind(service='db')

    def close_connection(self):
        self.db.close()

    def send_query(self, query):
        print(query)
        log = self.log.bind(event_id=str(uuid.uuid4()))
        log.msg(
            event='request',
            query=str(query)
        )
        allure.attach(
            f'Запрос: {query.compile(compile_kwargs={"literal_binds": True})}',
            name='request in DB',
            attachment_type=allure.attachment_type.TEXT
        )
        dataset = self.db.execute(statement=query).mappings().all()
        log.msg(
            event='response',
            dataset=[dict(row) for row in dataset]
        )
        allure.attach(
            str(dataset),
            name='response DB',
            attachment_type=allure.attachment_type.TEXT
        )
        return dataset

    def send_bulk_query(self, query):
        print(query)
        log = self.log.bind(event_id=str(uuid.uuid4()))
        log.msg(
            event='request',
            query=str(query)
        )
        allure.attach(
            f'Запрос: {query.compile(compile_kwargs={"literal_binds": True})}',
            name='request in DB',
            attachment_type=allure.attachment_type.TEXT
        )
        self.db.execute(statement=query)

