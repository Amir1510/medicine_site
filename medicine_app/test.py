import requests
import json

url = "http://127.0.0.1:8000/api/add_data/"
data = {
    "username": "John",
    "data": "Doe",
}


response = requests.post(url, data=data)
print(response)

