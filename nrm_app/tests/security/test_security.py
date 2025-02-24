import requests

def test_auth_incorrect_login():
    data = {"username": "username",
            "password": "password"}
    response = requests.post("http://localhost:5005/login", json=data)
    assert response.status_code == 401


def test_auth_correct_login():
    data = {"username": "admin",
            "password": "admin123",
            "kanapka": "moja"}
    response = requests.post("http://localhost:5005/login", json=data)
    assert response.status_code == 200


def test_xss():
    url = "http://localhost:5005/remove_with_folder"
    data = {"text": "<script>alert('XSS')</script>"}
    response = requests.post(url, json=data)
    assert "<script>" not in response.text
    assert response.status_code == 401