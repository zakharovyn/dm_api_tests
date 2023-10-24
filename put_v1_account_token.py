import requests


def put_v1_account_token():
    """
    Activate registered user
    :return:
    """
    token = '5f8e5013-61e9-4eb4-b8ab-a6351b43d69c'
    url = f"http://5.63.153.31:5051/v1/account/{token}"

    headers = {
      'X-Dm-Auth-Token': '<string>',
      'X-Dm-Bb-Render-Mode': '<string>',
      'Accept': 'text/plain'
    }

    response = requests.request(
        method="PUT",
        url=url,
        headers=headers
    )

    return response
