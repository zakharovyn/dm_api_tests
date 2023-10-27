import requests


def delete_v1_account_login_all():
    """
    Logout from every device
    :return:
    """
    url = "//v1/account/login/all"

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
