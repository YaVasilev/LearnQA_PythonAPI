import time

import allure
import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestUserDelete(BaseCase):

    @allure.description("В данном тесте проверяется, что нельзя удалить пользователя под id 2")
    def test_not_delete_user_by_id2(self):
        # LOGIN
        login_data = {
            'email': 'vinkotov@example.com',

            'password': '1234'
        }

        response = MyRequests.post("/user/login", data=login_data)

        Assertions.assert_code_status(response, 200)

        user_id = self.get_json_value(response, "user_id")
        auth_sid = self.get_cookie(response, "auth_sid")
        token = self.get_header(response, "x-csrf-token")

        # DELETE
        response2 = MyRequests.delete(f"/user/{user_id}",
                                      headers={"x-csrf-token": token},
                                      cookies={"auth_sid": auth_sid})

        Assertions.assert_code_status(response2, 400)
        Assertions.assert_response_text(response2, "Please, do not delete test users with ID 1, 2, 3, 4 or 5.")

        # LOGIN_ID_2
        response3 = MyRequests.get(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid})

        Assertions.assert_code_status(response3, 200)
        Assertions.assert_response_text(response3, '{"id":"2","username":"Vitaliy","email":"vinkotov@example.com","firstName":"Vitalii","lastName":"Kotov"}')

    @allure.description("В данном тесте проверяется возможность удаления пользователя после его создания")
    def test_delete_user_after_create(self):

        # REGISTRATION

        register_data = self.prepare_registration_data()

        response = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

        email = register_data["email"]
        first_name = register_data["firstName"]
        password = register_data["password"]
        user_id = self.get_json_value(response, "id")

        # LOGIN

        login_data = {
            "email": email,
            "password": password
        }

        response2 = MyRequests.post("/user/login", data=login_data)

        Assertions.assert_code_status(response2, 200)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # DELETE
        response3 = MyRequests.delete(f"/user/{user_id}",
                                      headers={"x-csrf-token": token},
                                      cookies={"auth_sid": auth_sid})

        Assertions.assert_code_status(response3, 200)

        # CHECK_USER
        response3 = MyRequests.get(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid})

        Assertions.assert_code_status(response3, 404)
        Assertions.assert_response_text(response3,"User not found")

    @allure.description("В данном тесте проверяется отсутствие возможности удаления пользователя из под другого пользователя")
    def test_delete_user_from_another_user(self):

        # REGISTER_USER_1
        register_data_user1 = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data_user1)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email_user1 = register_data_user1["email"]
        first_name_user1 = register_data_user1["firstName"]
        password_user1 = register_data_user1["password"]
        user_id_user1 = self.get_json_value(response1, "id")

        time.sleep(1)
        # LOGIN_USER_1
        login_data_user_1 = {
            "email": email_user1,
            "password": password_user1
        }

        response2 = MyRequests.post("/user/login", data=login_data_user_1)

        auth_sid_user1 = self.get_cookie(response2, "auth_sid")
        token_user1 = self.get_header(response2, "x-csrf-token")

        # REGISTER_USER_2
        register_data_user2 = self.prepare_registration_data()
        response3 = MyRequests.post("/user/", data=register_data_user2)

        Assertions.assert_code_status(response3, 200)
        Assertions.assert_json_has_key(response3, "id")

        email_user2 = register_data_user2["email"]
        first_name_user2 = register_data_user2["firstName"]
        password_user2 = register_data_user2["password"]
        user_id_user2 = self.get_json_value(response3, "id")

        # LOGIN_USER_2
        login_data_user_2 = {
            "email": email_user2,
            "password": password_user2
        }

        response4 = MyRequests.post("/user/login", data=login_data_user_2)

        auth_sid_user2 = self.get_cookie(response4, "auth_sid")
        token_user2 = self.get_header(response4, "x-csrf-token")

        # DELETE_USER_1_FROM_USER_2

        response5 = MyRequests.delete(f"/user/{user_id_user1}",
                                      headers={"x-csrf-token": token_user2},
                                      cookies={"auth_sid": auth_sid_user2})

        Assertions.assert_code_status(response5, 200)

        # CHECK_USER_1

        response6 = MyRequests.get(f"/user/{user_id_user1}",
                                   headers={"x-csrf-token": token_user1},
                                   cookies={"auth_sid": auth_sid_user1})

        Assertions.assert_code_status(response6, 200)
        Assertions.assert_json_value_by_name(response6, "id", user_id_user1, f"User with id: {user_id_user1} deleted")