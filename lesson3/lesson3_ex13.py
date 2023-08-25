import requests
import pytest


class TestUserAgent:
    url = "https://playground.learnqa.ru/ajax/api/user_agent_check"
    user_agents = {
        "user_agent_1": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0",
        "user_agent_2": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        "user_agent_3": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 OPR/101.0.0.0 (Edition Yx 03)",
        "user_agent_4": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36"
    }

    expected_result = {
        "result1": {
            "platform": "Web",
            "browser": "Firefox",
            "device": "No"
        },
        "result2": {
            "platform": "Web",
            "browser": "Chrome",
            "device": "No"
        },
        "result3": {
            "platform": "Web",
            "browser": "Chrome",
            "device": "No"
        },
        "result4": {
            "platform": "Mobile",
            "browser": "No",
            "device": "Android"
        }
    }

    agent_result = [
        (user_agents["user_agent_1"], expected_result["result1"]["platform"], expected_result["result1"]["browser"], expected_result["result1"]["device"]),
        (user_agents["user_agent_2"], expected_result["result2"]["platform"], expected_result["result2"]["browser"], expected_result["result2"]["device"]),
        (user_agents["user_agent_3"], expected_result["result3"]["platform"], expected_result["result3"]["browser"], expected_result["result3"]["device"]),
        (user_agents["user_agent_4"], expected_result["result4"]["platform"], expected_result["result4"]["browser"], expected_result["result4"]["device"])
    ]

    @pytest.mark.parametrize("user_agent, platform, browser, device", agent_result)
    def test_user_agent(self, user_agent, platform, browser, device):
        data = {"User-Agent": user_agent}
        response = requests.get(self.url, headers=data)

        actual_platform = response.json()["platform"]
        actual_browser = response.json()["browser"]
        actual_device = response.json()["device"]

        assert platform == actual_platform, f"Actual parameter is not equal expected parameter. Actual platform: {actual_platform}. Expected platform: {platform}"
        assert browser == actual_browser,f"Actual parameter is not equal expected parameter. Actual browser: {actual_browser}. Expected browser: {browser}"
        assert device == actual_device, f"Actual parameter is not equal expected parameter. Actual device: {actual_device}. Expected device: {device}"
