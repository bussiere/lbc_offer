import requests


r = requests.post(
    "http://54.38.92.164:8001/token-auth/",
    json={"Username": "bussiere", "Password": "rpgjdr09"},
)
print(r)
retur = r.json()
token = retur["Token"]


r = requests.post(
    "http://54.38.92.164:8001/getAllIngredientAlias/",
    json={
        "NbObject": 10,
        "NbPage": 1,
        "HasNoIngredientMatch": False,
        "SearchField": "Aqua",
        "Token": token,
    },
)
print(r.json())
