import requests

url = "http://192.168.88.9/api"

payload = {
    "cmd": "setuserinfo",
    "password": "1234",
    "enrollid": 3,
    "name": "Katriel",
    "department": "TI",
    "admin": 1,
    "pwd": 1234,
    "groupid": 1,
    "shiftid": 1,
    "starttime": "",
    "endtime": "",
    "birthday": "",
    "userprofile": "",
    "verifymode": 0,
    "zoneid": 0,
    "accesstimes": 0
}

r = requests.post(url, json=payload)

print(r.text)