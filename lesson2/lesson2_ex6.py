import requests

url = "https://playground.learnqa.ru/api/long_redirect"

response_long_redirect = requests.get(url, allow_redirects=True, verify=False)

first_response = response_long_redirect.history[0]
second_response = response_long_redirect

print(first_response.url)
print(second_response.url)
print("Redirect count:", len(response_long_redirect.history))