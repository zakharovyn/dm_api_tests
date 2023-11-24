from utilites import random_string
import pytest


@pytest.mark.parametrize('login, email, password, status_code, check', [
    ('Jack69', 'jack69@mail.ru', 'Jack69!Sparrow', 201, ''),
    (random_string(1, 12), random_string(1, 7) + '@mail.ru', random_string(1, 5), 400, {"Password": ["Short"]}),
    (random_string(1, 1), random_string(1, 14) + '@mail.ru', random_string(1, 40), 400, {"Login": ["Short"]}),
    (random_string(), 'jack69@', random_string(1, 50), 400, {"Email": ["Invalid"]}),
    (random_string(1, 15), 'jack69makarevich', random_string(), 400, {"Email": ["Invalid"]})
])
def test_create_and_activated_user_with_random_params(
        facade,
        orm,
        db,
        login,
        email,
        password,
        status_code,
        check
):
    orm.delete_user_by_login(login=login)
    facade.mailhog.delete_all_messages()

    response = facade.account.register_new_user(
        login=login,
        email=email,
        password=password,
        status_code=status_code
    )

    if status_code == 201:
        orm.update_activation_status(login=login, activation_status=True)
        dataset = orm.get_user_by_login(login=login)
        for row in dataset:
            assert row.Activated is True
    else:
        assert response.json()['errors'] == check, f'Некорректный ответ сервера: {response.json()["errors"]}'
