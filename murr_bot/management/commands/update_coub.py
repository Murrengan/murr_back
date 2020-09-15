import re

import requests
from murr_bot.models import Coub

search_tag = input("Что искать на коуб? (str с пробелами)")
page = input("Сколько парсить страниц (int)?")
per_page = input("Сколько выводить коубов на странице? (int)")

for _ in range(int(page)):
    response = requests.get(
        f'https://coub.com/api/v2/timeline/tag/{search_tag}?order_by=newest_popular&per_page={per_page}&page={_ + 1}').json()
    for i in response['coubs']:
        if i['file_versions']['share']['default'] is not None:
            title = [re.sub(r"[^a-zA-Z0-9]+", ' ', k) for k in i['title'].split("\n")][0]
            Coub.objects.create(
                title=title,
                likes_count=i['likes_count'],
                url=i['file_versions']['share']['default'],
                search_phrase='sexy girl'
            )
