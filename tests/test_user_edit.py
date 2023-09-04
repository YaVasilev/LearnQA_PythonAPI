import time

import allure

from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestUserEdit(BaseCase):

    def test_edit_just_created_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data["email"]
        first_name = register_data["firstName"]
        password = register_data["password"]
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            "email": email,
            "password": password
        }

        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_name = "Changed_name"

        response3 = MyRequests.put(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid},
                                   data={"firstName": new_name})

        Assertions.assert_code_status(response3, 200)

        # GET
        response4 = MyRequests.get(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid})

        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            new_name,
            "Wrong name of the user after edit"
        )

    # Ex17: Негативные тесты на PUT
    @allure.description("This test check editing user without logining")
    def test_edit_user_details_wo_auth(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        user_id = self.get_json_value(response1, "id")

        # EDIT
        new_name = "Test_Name"

        response2 = MyRequests.put(f"/user/{user_id}", data={"firstName": new_name})

        Assertions.assert_code_status(response2, 400)
        Assertions.assert_response_text(response2, "Auth token not supplied")

    @allure.description("Проверка невозможности изменения одного пользователя из под другого")
    def test_edit_user_from_auth_another_user(self):
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

        # REGISTER_USER_2
        register_data_user2 = self.prepare_registration_data()
        response2 = MyRequests.post("/user/", data=register_data_user2)

        Assertions.assert_code_status(response2, 200)
        Assertions.assert_json_has_key(response2, "id")

        email_user2 = register_data_user2["email"]
        first_name_user2 = register_data_user2["firstName"]
        password_user2 = register_data_user2["password"]
        user_id_user2 = self.get_json_value(response2, "id")

        # LOGIN_USER_2
        login_data = {
            "email": email_user2,
            "password": password_user2
        }

        response3 = MyRequests.post("/user/login", data=login_data)

        auth_sid_user2 = self.get_cookie(response3, "auth_sid")
        token_user2 = self.get_header(response3, "x-csrf-token")

        # EDIT USER_1 from USER_2
        new_name = "Test_Name2"

        response4 = MyRequests.put(f"/user/{user_id_user1}",
                                   headers={"x-csrf-token": auth_sid_user2},
                                   cookies={"auth_sid": token_user2},
                                   data={"firstName": new_name})

        Assertions.assert_code_status(response4, 400)
        Assertions.assert_response_text(response4, "Auth token not supplied")

        # LOGIN_USER_1
        login_data = {
            "email": email_user1,
            "password": password_user1
        }

        response5 = MyRequests.post("/user/login", data=login_data)

        auth_sid_user1 = self.get_cookie(response5, "auth_sid")
        token_user1 = self.get_header(response5, "x-csrf-token")

        # CHECK NOT EDITED USER_1
        response6 = MyRequests.get(f"/user/{user_id_user1}",
                                   headers={"x-csrf-token": token_user1},
                                   cookies={"auth_sid": auth_sid_user1})

        Assertions.assert_json_value_by_name(response6, "firstName", first_name_user1,
                                             "Wrong name of the user after incorrect edit. 'firstName' must not be "
                                             "edited")

    @allure.description("This test check email, after put wo dog symbol")
    def test_edit_email_after_auth_wo_dog_symbol(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data["email"]
        first_name = register_data["firstName"]
        password = register_data["password"]
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            "email": email,
            "password": password
        }

        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_email = "Testexample.com"

        response3 = MyRequests.put(f"/user/{user_id}", headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid},
                                   data={"email": new_email})

        Assertions.assert_code_status(response3, 400)
        Assertions.assert_response_text(response3, "Invalid email format")

    @allure.description("This test check change firstName on no valid, after auth")
    def test_edit_firstname_after_auth_to_no_valid(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data["email"]
        first_name = register_data["firstName"]
        password = register_data["password"]
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            "email": email,
            "password": password
        }

        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_name = "T"

        response3 = MyRequests.put(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid},
                                   data={"firstName": new_name})

        Assertions.assert_code_status(response3, 400)
        Assertions.assert_response_text(response3, '{"error":"Too short value for field firstName"}')
