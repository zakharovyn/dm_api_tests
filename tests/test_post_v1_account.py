from services.dm_api_account import DmApiAccount


def test_post_v1_account():
    api = DmApiAccount(host='http://5.63.153.31:5051')
    json = {
        "login": "new_user2",
        "email": "new_user2@email.com",
        "password": "new_user2"
    }
    response = api.account.post_v1_account(
        json=json
    )
