import requests


r = requests.post("http://127.0.0.1:8091/getOfferFromHash/",json={"Geohash":"u09tvnrbtbt3w3st","NbMinuteCar":30,"NbMinuteWalk":30})
print(r.json())