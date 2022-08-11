import requests as req
import os
from dotenv import load_dotenv

load_dotenv()


class Test:
    def __init__(self):
        self.host = os.getenv("HOST")
        self.email = "test@mail.com"
        self.password = "test"
        self.token = None
        self.admin_secret_key = os.getenv("SECRET_KEY")
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        self.todo = {
            "title": "test",
            "description": "test",
        }

        # try:
        self.remove_test_user_if_exists()
        # except:
        #     raise Exception('Failed to remove test user')

    def remove_test_user_if_exists(self):
        req.get(
            self.host + "/auth/remove_user",
            params={"email": self.email, "admin_secret_key": self.admin_secret_key},
        )

    def set_token(self):
        resp = req.get(
            self.host + "/auth/login",
            params={"email": self.email, "password": self.password},
        )
        self.token = resp.json()["token"]
        self.headers["Authorization"] = "Bearer " + self.token


test = Test()
