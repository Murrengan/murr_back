<p align="center">
<img src="../img/thumbnail.png" align="center" title="Murrengan network"/>
</p>

<a href="../../../../"><img src="../img/russian_federation.png" align="right" height="25" width="30" title="Русский"></a>

<h2 align="center">Murrengan provide core functionality for web applications:</h2>

<ul>
    <li>user registration (0.0.12b)</li>
    <li>getting information from client (0.0.13)</li>
    <li>chat application (in dev)</li>
    <li>cart and payments (in plan)</li>
</ul>

<h3 align="center">For ease of use there are 2 main branches:</h3>

<b>[master](https://github.com/Murrengan/murr_front/tree/master)</b> - Main branch, the result of which can be seen at the link http://www.murrengan.ru/.

<b>[develop](https://github.com/Murrengan/murr_front/tree/develop)</b> - Branch for developers. Checkout from here and implement new features</b>.

<h2 align="center">In developing used:</h2>

* [Python 3.6.9](https://www.python.org/downloads/release/python-369/)
* [Django 3](https://www.djangoproject.com/) as main backend framework
* [Django REST](https://www.django-rest-framework.org/) for building Web APIs
* [Simplejwt](https://github.com/davesque/django-rest-framework-simplejwt) for JSON Web Token authentication

### Setup
```
pip install -r requirements.txt
```
##### Migrations
```
python manage.py migrate
```

##### Prepare test data - like admin user and etc
```
python manage.py prepare_stand
```

##### Run for development
```
python manage.py runserver
```


##### Run tests
```
pytest
```

### Run on prod via Docker
```
Make a file entrypoint.sh executable (sudo chmod +x entrypoint.sh)
Run sudo docker-compose up --build (-d for detach mode)
For https, get origin_ca_rsa_root.pem and private_origin_ca_ecc_root.pem certificates from cloudflare.com and place them in . / nginx
```
### Run on dev via Docker
```
Make a file entrypoint.sh executable (sudo chmod +x entrypoint.sh)
Run docker-compose -f docker-compose-dev.yml up --build (-d for detach mode)
```
#### If you are on windows, make sure that entrypoint.sh should line separator LF instead of CRLF (can be changed in pycharm )
<br/>

<h2 align="center">Download, train and take part in improving the functionality!❤</h2>


# 🌟Support🌟 
[click](http://bit.do/eWnnm)

<h4>Contacts:</h4>

[Telegram](https://tlgg.ru/MurrenganChat)<br/>
[Youtube](https://youtube.com/murrengan/)<br/>
[VK](https://vk.com/murrengan)<br/>
[Site](https://www.murrengan.ru/)
