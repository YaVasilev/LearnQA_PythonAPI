import requests

url = "https://playground.learnqa.ru/api/homework_header"


def test_header_value():
    response = requests.get(url)
    print(response.headers["x-secret-homework-header"])
    header = "Some secret value"
    assert response.headers[
               "x-secret-homework-header"] == header, f"Response header x-secret-homework-header is not equal {header} "
