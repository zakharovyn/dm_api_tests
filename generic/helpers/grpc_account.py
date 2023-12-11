from apis.dm_api_search.account_pb2 import RegisterAccountRequest
from apis.dm_api_search.dm_grpc_account import DmGrpcAccount


class GrpcAccount:
    def __init__(self, target):
        self.grpc_account = DmGrpcAccount(target=target)

    def register_account(self, login: str, email: str, password: str):
        response = self.grpc_account.register_account(
            request=RegisterAccountRequest(
                login=login,
                email=email,
                password=password
            )
        )
        return response

    def close(self):
        self.grpc_account.channel.close()
