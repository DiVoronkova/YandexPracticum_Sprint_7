import requests
import allure
from url import URL


class OrderMethods:

    @staticmethod
    @allure.step('Создать заказ')
    def create_order(body):
        return requests.post(url=URL.CREATE_ORDER, json=body)
    
    @staticmethod
    @allure.step('Получить список заказов')
    def get_order_list():
        return requests.get(url=URL.ORDER_LIST)