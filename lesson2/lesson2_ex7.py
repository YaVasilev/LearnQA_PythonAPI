import requests

url = "https://playground.learnqa.ru/ajax/api/compare_query_type"

"""Запрос без параметра method"""
response_compare_query_type_get = requests.get(url, verify=False)
print("Запрос без параметра")
print("Код ответа:", response_compare_query_type_get.status_code)
print("Текст ответа:", response_compare_query_type_get.text, "\n")

"""Запрос с параметром HEAD"""
paylod_head = {"method": "HEAD"}
response_compare_query_type_head = requests.head(url, data=paylod_head, verify=False)
print(f"Запрос с параметром HEAD")
print("Код ответа:", response_compare_query_type_head.status_code)
print("Текст ответа:", response_compare_query_type_head.text, "\n")

"""Запрос с правильным параметром POST"""
paylod_post = {"method": "POST"}
response_compare_query_type_post = requests.post(url, data=paylod_post, verify=False)
print(f"Запрос с параметром POST")
print("Код ответа:", response_compare_query_type_post.status_code)
print("Текст ответа:", response_compare_query_type_post.text, "\n")

"""Проверка сочетания реальных типов запроса и значений параметра method"""
methods = ["GET", "PUT", "POST", "DELETE", "Error", ""]
print("Проверка сочетания реальных типов запроса и значений параметра method")

for method in methods:
    response_get = requests.get(url, params={"method": f"{method}"})
    print(f"GET запрос с методом: {method}")
    print("Код ответа:", response_get.status_code)
    print("Текст ответа:", response_get.text,"\n")

    response_put = requests.put(url, data={"method": f"{method}"})
    print(f"PUT запрос с методом: {method}")
    print("Код ответа:", response_put.status_code)
    print("Текст ответа:", response_put.text,"\n")

    response_post = requests.post(url, data={"method": f"{method}"})
    print(f"POST запрос с методом: {method}")
    print("Код ответа:", response_post.status_code)
    print("Текст ответа:", response_post.text,"\n")

    response_delete = requests.delete(url, data={"method": f"{method}"})
    print(f"DELETE запрос с методом: {method}")
    print("Код ответа:", response_delete.status_code)
    print("Текст ответа:", response_delete.text,"\n")

