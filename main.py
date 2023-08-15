import requests

print("Hello from Yaroslav")

response = requests.get('https://playground.learnqa.ru/api/hello', verify=False)
print(response.text)
