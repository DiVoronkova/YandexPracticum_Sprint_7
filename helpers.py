from data import DataForLogin


def modify_data_for_login(key, value):
    body = DataForLogin.CREATE_DATA_FOR_LOGIN.copy()
    body[key] = value
    return body
