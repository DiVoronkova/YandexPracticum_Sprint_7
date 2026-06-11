import pytest
from api_methods.courier_methods import CourierMethods
from generators import generate_courier_body


@pytest.fixture
def delete_courier_after_test():
    create_courier_data = []
    yield create_courier_data
    if create_courier_data:
        body = create_courier_data[0]
        body_for_login = {"login": body["login"], "password": body["password"]}
        login_response = CourierMethods.login_courier(body_for_login)
        if login_response.status_code == 200:
            courier_id = login_response.json()["id"]
            delete_response = CourierMethods.delete_courier(courier_id)
            assert delete_response.status_code == 200, f"Ожидалось 200 при удалении, но получено {delete_response.status_code}"
            assert delete_response.json()["ok"] is True, "Поле 'ok' должно быть True после удаления"
    
        else:
            print(f"Не удалось авторизоваться для удаления курьера. Статус: {login_response.status_code}, "f"Ответ: {login_response.json()}")


@pytest.fixture
def create_and_delete_courier():
    # Создание курьера
    body = generate_courier_body()
    create_response = CourierMethods.create_courier(body)
    assert create_response.status_code == 201, f"Ошибка создания курьера: {create_response.status_code}"

    # Авторизация для получения ID
    login_data = {
        "login": body["login"],
        "password": body["password"]
    }
    login_response = CourierMethods.login_courier(login_data)
    assert login_response.status_code == 200, f"Ошибка авторизации: {login_response.status_code}"
    courier_id = login_response.json()["id"]

    # Возвращаем данные курьера и его ID
    yield {
        "login": body["login"],
        "password": body["password"],
        "id": courier_id
    }

    # Удаление курьера после теста
    delete_response = CourierMethods.delete_courier(courier_id)
    if delete_response.status_code != 200:
        print(f"Предупреждение: не удалось удалить курьера с ID {courier_id}. "
              f"Статус: {delete_response.status_code}, ответ: {delete_response.json()}")

