import requests


while True:
    try:
        req = requests.get("http://localhost/", timeout=0.01)
        print(req.status_code)
    except requests.exceptions.ReadTimeout:
        pass