from unittest import TestCase
import requests
import random

user_name = "test_user_{0}".format(random.randint(1, 1e6))
key_name = "test_key_{0}".format(random.randint(1, 1e6))
key = "apple"

url = "http://127.0.0.1:8000"

class DjangoTestCase(TestCase):
    def test_register_user(self):
        print("1")
        endpoint = "/api/register/"
        data = {
            "username": user_name,
            "email": "{0}@example.com".format(user_name),
            "password": "Test_password@123",
            "full_name": "Test User",
            "age": 30,
            "gender": "male"
        }
        print(url+endpoint, data)
        response = requests.post(url + endpoint, json=data)
        print(response.status_code)
        assert response.status_code == 200
        assert response.json()["message"] == "User successfully registered!"

    def test_generate_token(self): 
        endpoint = "/api/token/"
        data = {
            "username": user_name,
            "password": "Test_password@123"
        }
        response = requests.post(url + endpoint, json=data)
        print("response", response.request.url, response.request.method, response.status_code, response.text)
        assert response.status_code == 200
        assert response.json()["message"] == "Access token generated successfully."
        return {"Authorization": format(response.json()['data']['access_token'])}

    def test_store_data(self):
        endpoint = "/api/data/"
        data = {
            "key": key_name,
            "value": "test_value"
        }
        response = requests.post(url + endpoint, json=data, headers=self.test_generate_token())
        print(url+endpoint, self.test_generate_token())
        print("response", response.request.url, response.request.method, response.status_code, response.text, )
        assert response.status_code == 200
        assert response.json()["message"] == "Data stored successfully."

    def test_retrieve_data(self):
        endpoint = "/api/data/{0}/".format(key_name)
        response = requests.get(url + endpoint, headers=self.test_generate_token())
        print("response", response.request.url, response.request.method, response.status_code, response.text)
        assert response.status_code == 200
        assert response.json()["data"]["key"] == key_name
        # assert response.json()["data"]["value"] == "fruit"

    def test_update_data(self):
        endpoint = "/api/data/{0}/".format(key_name)
        data = {
            "value": "new_test_value"
        }
        print(url+endpoint, self.test_generate_token())
        response = requests.put(url + endpoint, json=data, headers=self.test_generate_token())
        print("response", response.request.url, response.request.method, response.status_code)
        assert response.status_code == 200
        assert response.json()["message"] == "Data updated successfully."
            

    def test_delete_data(self):
        endpoint = "/api/data/{0}".format(key_name)
        response = requests.delete(url + endpoint, headers=self.test_generate_token())
        print("response", response.request.url, response.request.method, response.status_code, response.text)
        assert response.status_code == 200
        assert response.json()["message"] == "Data deleted successfully."
        
    def test_all(self):
        self.test_register_user()
        self.test_generate_token()
        self.test_store_data()
        self.test_retrieve_data()
        self.test_update_data()
        self.test_delete_data()

    if __name__ == "__main__":
        test_all()
