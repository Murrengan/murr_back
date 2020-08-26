import json
import re

import requests

data_to_write = []

search_phrase = 'ahegao'
per_page = 100
page = 4
db_json_file_name = 'ahegao_db.json'

for _ in range(page):
    response = requests.get(
        f'https://coub.com/api/v2/search?q={search_phrase}&order_by=likes_count&per_page={per_page}&page={_ + 1}').json()
    for i in response['coubs']:
        if i['file_versions']['share']['default'] is not None:
            title = [re.sub(r"[^a-zA-Z0-9]+", ' ', k) for k in i['title'].split("\n")][0]
            data_to_write.append({
                'title': title,
                'likes_count': i['likes_count'],
                'url': i['file_versions']['share']['default'],
                'search_phrase': search_phrase
            })

with open(db_json_file_name, 'w') as file:
    json.dump(data_to_write, file)
