from restclient.restclient import Restclient
from requests import Response
import json
import time


class MailhogApi:

    def __init__(self, host='http://5.63.153.31:5025'):
        self.host = host
        self.client = self.client = Restclient(host=host)

    def get_api_v2_messages(self, limit: int = 50) -> Response:
        """
        Get messages by limit
        :param limit:
        :return:
        """
        response = self.client.get(
            path=f"/api/v2/messages",
            params={
                'limit': limit
            }
        )

        return response

    def get_token_from_last_email(self, reset_password: bool = False) -> str:
        """
        Get user activation token from last email
        :return:
        """
        time.sleep(2)
        email = self.get_api_v2_messages(limit=1).json()
        if reset_password is False:
            token_url = json.loads(email['items'][0]['Content']['Body'])['ConfirmationLinkUrl']
        else:
            token_url = json.loads(email['items'][0]['Content']['Body'])['ConfirmationLinkUri']

        token = token_url.split('/')[-1]

        return token
