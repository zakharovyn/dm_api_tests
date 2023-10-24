import requests


def delete_v1_account_login():
    """
    Logout as current user
    :return:
    """
    url = "http://5.63.153.31:5051/v1/account/login"

    headers = {
      'X-Dm-Auth-Token': '<string>',
      'X-Dm-Bb-Render-Mode': '<string>',
      'Accept': 'text/plain'
    }

    response = requests.request(
        method="DELETE",
        url=url,
        headers=headers
    )

    return response
