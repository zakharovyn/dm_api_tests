from apis.dm_grpc_account_async import RegisterAccountRequest
from apis.dm_grpc_account_async import AccountServiceStub
from grpclib.client import Channel
import pytest


def test_search(grpc_account):

    response = grpc_account.register_account(
        login='petr2',
        email='petr2@sobaka.ru',
        password='petrpes'
    )
    print(response)


@pytest.mark.asyncio
async def test_register_account_async():
    channel = Channel(host='5.63.153.31', port=5055)
    async_grpc = AccountServiceStub(channel=channel)

    response = await async_grpc.register_account(
        register_account_request=RegisterAccountRequest(
            login='petr_3',
            email='petr_3@sobaka.ru',
            password='petr-pes'
        )
    )
    print(response)
