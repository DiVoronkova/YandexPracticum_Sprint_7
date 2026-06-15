import requests
import allure
from url import URL


class CourierMethods:

    @staticmethod
    @allure.step('Залогинить курьера в системе')
    def login_courier(body):
        return requests.post(url=URL.LOGIN_COURIER, json=body)

    @staticmethod
    @allure.step('Создать курьера')
    def create_courier(body):
        return requests.post(url=URL.CREATE_COURIER, json=body)
    
    @staticmethod
    @allure.step('Удалить курьера')
    def delete_courier(courier_id):
        return requests.delete(url=f"{URL.CREATE_COURIER}/{courier_id}")
