import requests


r = requests.post("http://127.0.0.1:8091/getOfferFromHash/",json={"GeoHash1":"u09u402gggqe","GeoHash2":"u09ydhk203p5"})
print(r)
print(r.json())