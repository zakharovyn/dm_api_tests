

def test_post_v1_account_password(facade, orm, prepare_user):
    login = prepare_user.login
    email = prepare_user.email
    password = prepare_user.password

    orm.delete_user_by_login(login=login)

    dataset = orm.get_user_by_login(login=login)
    assert len(dataset) == 0

    facade.account.register_new_user(
        login=login,
        email=email,
        password=password
    )

    dataset = orm.get_user_by_login(login=login)
    for row in dataset:
        assert row.Login == login
        assert row.Activated is False

    orm.update_activation_status(login=login, activation_status=True)

    dataset = orm.get_user_by_login(login=login)
    for row in dataset:
        assert row.Activated is True

    token = facade.login.get_auth_token(
        login=login,
        password=password
    )

    facade.account.set_headers(headers=token)

    facade.account.reset_registered_user_password(
        login=login,
        email=email
    )

    new_token = facade.mailhog.get_token_by_login(
        login=login,
        reset_password=True
    )

    assert token != new_token
