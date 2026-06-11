import allure
import pytest

from api_methods.courier_methods import CourierMethods
from generators import generate_courier_body


class TestCreateCourier:
    
    @allure.title("Тест создания нового курьера")
    @allure.description("""Тест проверяет успешное создание курьера с использованием валидных данных. 
                        Ожидается:
                        статус‑код 201;
                        значение поля ok в ответе равно True.""")
    def test_create_courier_success(self, delete_courier_after_test):
        body = generate_courier_body()
        response = CourierMethods.create_courier(body)
        response_data = response.json()
        assert response.status_code == 201, f"Ожидалось 201, но получено {response.status_code}"
        assert response_data["ok"] == True, "Поле 'ok' должно быть True"
        with allure.step("Добавляем данные созданного курьера в список для последующего удаления."):
            delete_courier_after_test.append(body)


    @allure.title("Тест создания курьера с некорректными данными: {invalid_field} пуст")
    @allure.description("""Проверяется создание курьера с пустым значением в поле {invalid_field}. 
                        Ожидается: 
                        статус‑код 400;
                        cообщение: «Недостаточно данных для создания учётной записи».""")
    @pytest.mark.parametrize("invalid_field, invalid_value",
    [
        ("login", ""),
        ("password", ""),
        ("first_name", ""),  
    ])
    def test_create_courier_empty_field_shows_error(self, invalid_field, invalid_value):
        body = generate_courier_body()
        with allure.step(f"Подготовка данных: устанавливаем пустое значение для поля {invalid_field}"):
            body[invalid_field] = invalid_value
        with allure.step("Отправка запроса на создание курьера"):
            response = CourierMethods.create_courier(body)
            response_data = response.json()
        with allure.step("Проверка результатов"):
            assert response.status_code == 400, f"Ожидался статус 400, но получено {response.status_code}"
            assert response_data["message"] == "Недостаточно данных для создания учетной записи", f"Текст сообщения отсутствует или не совпадает: {response_data['message']}"


    @allure.title("Тест создания курьера с повторяющимся логином")
    @allure.description("""Тест проверяет обработку попытки создания курьера с логином, который уже зарегистрирован в системе. 
                        Ожидается: 
                        статус‑код 409 (Conflict);
                        сообщение об ошибке: «Этот логин уже используется».""")
    def test_create_courier_duplicate_login_shows_error(self, delete_courier_after_test):
        with allure.step("Создаём первого курьера с определённым логином"):
            first_body = generate_courier_body()
            first_courier = CourierMethods.create_courier(first_body)
            assert first_courier.status_code == 201, f"Ожидался статус-код 201 (Created), но получено {first_courier.status_code}"
        with allure.step("Попытка создать второго курьера с тем же логином"):
            second_courier = CourierMethods.create_courier(first_body)
            response_data = second_courier.json()
            assert second_courier.status_code == 409, f"Ожидался статус-код 409, но получено {second_courier.status_code}"
            assert response_data["message"] == "Этот логин уже используется", f"Текст сообщения отсутствует или не совпадает: {response_data['message']}"
        with allure.step("Добавляем данные первого курьера в список для последующего удаления."):
            delete_courier_after_test.append(first_body)

