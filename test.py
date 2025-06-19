import requests
import json

url_r = 'http://127.0.0.1:5000/register'
url_l = 'http://127.0.0.1:5000/login'
register = {
    "username": "aaaaaaaa",
    "password": "12345678",
    "confirm_password": "12345678",
    "role": "admin"
}
login = {"username": "abcdef_", "password": "12345678"}
r = requests.post(url_l, json=login)
print(r.json())
