import allure
import pytest

from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


@allure.epic("Register cases")
class TestUSerRegister(BaseCase):

    @allure.description("This test successfully create new user")
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    @allure.description("This test check users with existing email")
    def test_create_user_with_existing_email(self):
        email = "vinkotov@example.com"
        data = self.prepare_registration_data(email=email)

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content {response.content}"

    # Home tasks Ex15: Тесты на метод user
    @allure.description("This test check creating users without dog symbol in email")
    def test_create_user_without_dog_symbol_in_email(self):
        email = "testexample.com"
        data = self.prepare_registration_data(email=email)

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Invalid email format", f"Response: {response.content}"

    fields = {
        'password',
        'username',
        'firstName',
        'lastName',
        'email'
    }

    @allure.description("This test check creating users without field in request")
    @pytest.mark.parametrize("missing_field", fields)
    def test_create_user_wo_one_field_in_creating_form(self, missing_field):
        data = self.prepare_registration_data()
        data.pop(missing_field, None)

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The following required params are missed: {missing_field}", \
            f"Response: {response.content}"

    names = {
        "T",
        "TestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTest"
        "TestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTest"
        "TestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTest"
        "TestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTest"
    }

    @allure.description("This test check creating users with short and long names")
    @pytest.mark.parametrize("name", names)
    def test_create_user_with_short_and_long_name(self, name):
        data = self.prepare_registration_data(username=name)

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 400)
        if len(name) == 1:
            assert response.content.decode("utf-8") == "The value of 'username' field is too short"
        elif len(name) > 250:
            assert response.content.decode("utf-8") == "The value of 'username' field is too long"