import pytest
import logging

from api_methods.courier_methods import CourierMethods
from generators import generate_courier_body


logger = logging.getLogger(__name__)

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
            CourierMethods.delete_courier(courier_id)
        else:
            logger.error(
                "Не удалось авторизоваться для удаления курьера. Статус: %s, Ответ: %s",
                login_response.status_code,
                login_response.json()
            )


@pytest.fixture
def create_and_delete_courier():
    # Создание курьера
    body = generate_courier_body()
    CourierMethods.create_courier(body)

    # Авторизация для получения ID
    login_data = {
        "login": body["login"],
        "password": body["password"]
    }
    login_response = CourierMethods.login_courier(login_data)
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
        logger.warning(
            "Не удалось удалить курьера с ID %s. Статус: %s, Ответ: %s",
            courier_id,
            delete_response.status_code,
            delete_response.json()
        )
