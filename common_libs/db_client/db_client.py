import structlog
import records
import allure
import uuid


class DbClient:

    def __init__(self, user, password, host, database, isolation_level='AUTOCOMMIT'):
        connection_string = f"postgresql://{user}:{password}@{host}/{database}"
        self.db = records.Database(connection_string, isolation_level=isolation_level)
        self.log = structlog.get_logger(self.__class__.__name__).bind(service='db')

    def send_query(self, query: str):
        print(query)
        log = self.log.bind(event_id=str(uuid.uuid4()))
        log.msg(
            event='request',
            query=query
        )
        allure.attach(
            query,
            name='request in DB',
            attachment_type=allure.attachment_type.TEXT
        )
        dataset = self.db.query(query=query).as_dict()
        log.msg(
            event='response',
            dataset=dataset
        )
        allure.attach(
            str(dataset),
            name='response DB',
            attachment_type=allure.attachment_type.TEXT
        )
        return dataset

    def send_bulk_query(self, query: str):
        print(query)
        log = self.log.bind(event_id=str(uuid.uuid4()))
        log.msg(
            event='request',
            query=query
        )
        allure.attach(
            query,
            name='request in DB',
            attachment_type=allure.attachment_type.TEXT
        )
        self.db.bulk_query(query=query)

