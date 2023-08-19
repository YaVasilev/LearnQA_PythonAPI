import requests

url = "https://playground.learnqa.ru/ajax/api/compare_query_type"


def print_response(response):
    print("Код ответа:", response.status_code)
    print("Текст ответа:", response.text, "\n")


"""Запрос без параметра method"""
response_compare_query_type_get = requests.get(url, verify=False)
print("Запрос без параметра")
print_response(response_compare_query_type_get)

"""Запрос с параметром HEAD"""
paylod_head = {"method": "HEAD"}
response_compare_query_type_head = requests.head(url, data=paylod_head, verify=False)
print(f"Запрос с параметром HEAD")
print_response(response_compare_query_type_head)

"""Запрос с правильным параметром POST"""
paylod_post = {"method": "POST"}
response_compare_query_type_post = requests.post(url, data=paylod_post, verify=False)
print(f"Запрос с параметром POST")
print_response(response_compare_query_type_post)

"""Проверка сочетания реальных типов запроса и значений параметра method"""
methods = ["GET", "PUT", "POST", "DELETE", "Error", ""]
print("Проверка сочетания реальных типов запроса и значений параметра method")

for method in methods:
    response_get = requests.get(url, params={"method": f"{method}"})
    print(f"GET запрос с методом: {method}")
    print_response(response_get)

    response_put = requests.put(url, data={"method": f"{method}"})
    print(f"PUT запрос с методом: {method}")
    print_response(response_put)

    response_post = requests.post(url, data={"method": f"{method}"})
    print(f"POST запрос с методом: {method}")
    print_response(response_post)

    response_delete = requests.delete(url, data={"method": f"{method}"})
    print(f"DELETE запрос с методом: {method}")
    print_response(response_delete)