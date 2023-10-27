from services.dm_api_account import DmApiAccount


def test_put_v1_account_token():
    api = DmApiAccount(host='http://5.63.153.31:5051')

    token = '444ed273-0574-41c5-a385-c8bd60af4ec1' # нужен метод для получения токена

    response = api.account.put_v1_account_token(
        token=token
    )
