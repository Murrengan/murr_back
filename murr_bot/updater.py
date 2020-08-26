import json

data = []
with open('ahegao_db.json', 'r') as file:
    coubs = json.loads(file.read())

for coub in coubs:
    data.append({
        "model": "murr_bot.coub",
        "pk": coubs.index(coub) + 2200,
        "fields": coub
    })

with open('ahegao_db.json', 'w') as file:
    json.dump(data, file)
