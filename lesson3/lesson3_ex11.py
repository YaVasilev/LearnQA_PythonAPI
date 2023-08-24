import requests

url = "https://playground.learnqa.ru/api/homework_cookie"


def test_cookie_number():
    response = requests.get(url)
    response_cookie = response.cookies["HomeWork"]
    print(response.cookies)
    cookie = "hw_value"
    assert response.status_code == 200, f"Response status code is not equal 200"
    assert response_cookie == cookie, f"Cookie is not equal {cookie}"
