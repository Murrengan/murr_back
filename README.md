<p align="center">
<img src="readme/img/thumbnail.png" align="center" title="Murrengan network"/>
</p>

![Python application](https://github.com/semenInRussia/murr_back/workflows/Python%20application/badge.svg)

<a href="readme/en"><img src="readme/img/united_states_of_america_usa.png" align="right" height="25" width="30" title="English"></a>
<br/>

<h3 align="center">Мурренган предоставляет базовый набор функций для веб приложений:</h3>

<ul>
    <li>Регистрация клиента на сайте (доступно с версии 0.0.12b)</li>
    <li>Получение информации от клиента (доступно с версии 0.0.13)</li>
    <li>Чат (в разработке)</li>
    <li>Корзина товаров и оплата (в планах)</li>
</ul>

<h3 align="center">Для удобства использования существует 2 бранча:</h3>

<b>[master](https://github.com/Murrengan/murr_front/tree/master)</b> - Основная ветка, результат работы которой можно найти по ссылке https://www.murrengan.ru/.

<b>[develop](https://github.com/Murrengan/murr_front/tree/develop)</b> - Ветка для разработчиков. Новый функционал вливается сюда</b>.

<h2 align="center">В разработке применяется:</h2>

* [Python 3.6.9](https://www.python.org/downloads/release/python-369/)
* [Django 3](https://www.djangoproject.com/) как основной фреймворк для бекенда
* [Django REST](https://www.django-rest-framework.org/) для создания rest api
* [Simplejwt](https://github.com/davesque/django-rest-framework-simplejwt) для аутентификации через JSON Web Token

### Установка
```
pip install -r requirements.txt
```
### Подготовка базы данных
```
python manage.py makemigrations murren murr_card
python manage.py migrate
```

### Запуск сервера
```
python manage.py runserver
```

### Запуск тестов
```
pytest
```

<br/>

<h2 align="center">Скачивай, тренируйся и принимай участие в улучшении функционала!❤</h2>

# 🌟Поддержать проект🌟 
[click](http://bit.do/eWnnm)

<h4>Контакты:</h4>

[Telegram](https://tlgg.ru/MurrenganChat)<br/>
[Youtube](https://youtube.com/murrengan/)<br/>
[VK](https://vk.com/murrengan)<br/>
[Site](https://www.murrengan.ru/)
