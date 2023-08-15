import requests

print("Hello from Yaroslav")

response = requests.get('https://playground.learnqa.ru/api/get_text', verify=False)
print(response.text)
