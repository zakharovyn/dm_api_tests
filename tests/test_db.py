from generic.helpers.dm_db import DmDatabase
import structlog

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


def test_db():

    db = DmDatabase(user='postgres', password='admin', host='5.63.153.31', database='dm3.5')
    # db.get_all_users()
    db.update_activation_status(login='new_user106', activation_status='false')
