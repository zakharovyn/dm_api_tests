

def test_post_v1_account_password(facade, orm, prepare_user, assertions):
    login = prepare_user.login
    email = prepare_user.email
    password = prepare_user.password

    facade.account.register_new_user(login=login, email=email, password=password)
    assertions.check_user_was_created(login=login)

    orm.update_activation_status(login=login, activation_status=True)
    assertions.check_user_war_activated(login=login)

    token = facade.login.get_auth_token(login=login, password=password)
    facade.account.set_headers(headers=token)

    facade.account.reset_registered_user_password(login=login, email=email)

    new_token = facade.mailhog.get_token_by_login(login=login, reset_password=True)
    assert token != new_token
