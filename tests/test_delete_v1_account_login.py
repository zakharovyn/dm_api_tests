

def test_delete_v1_account_login(facade, orm, prepare_user, assertions):
    login = prepare_user.login
    email = prepare_user.email
    password = prepare_user.password

    facade.account.register_new_user(login=login, email=email, password=password)
    assertions.check_user_was_created(login=login)

    dataset = orm.get_user_by_login(login=login)
    for row in dataset:
        assert row.Login == login
        assert row.Activated is False

    orm.update_activation_status(login=login, activation_status=True)
    assertions.check_user_war_activated(login=login)

    token = facade.login.get_auth_token(login=login,password=password)
    facade.login.set_headers(headers=token)
    facade.login.logout_user()
