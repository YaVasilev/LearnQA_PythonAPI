import requests
import time
import json

url = "https://playground.learnqa.ru/ajax/api/longtime_job"

"""Отправляем запрос и получаем token"""
response_without_get_params = requests.get(url, verify=False)
obj = json.loads(response_without_get_params.text)
token = obj["token"]
seconds = obj["seconds"]
print("Код ответа:", response_without_get_params.status_code)
print("Текст ответа:", response_without_get_params.text, "\n")
time.sleep(seconds)

"""Отправляем запрос с полученным  token"""
payload = {"token": token}
response_with_get_token = requests.get(url, params=payload, verify=False)
print("Код ответа:", response_with_get_token.status_code)
print("Текст ответа:", response_with_get_token.text)
