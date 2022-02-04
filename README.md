# Запуск
### для запуска используйте docker-compose:
``` docker-compose up ```
Eсли вы не добавили себя в группу пользователей docker -добавьте в начале sudo.
### миграции будут произведены автоматически,так же как и тесты.
####  будет создан супер пользователь с данными:
```
DJANGO_SUPERUSER_PASSWORD=adminAdm1n
DJANGO_SUPERUSER_USERNAME=admin
```
Для ручного запуска тестов необходимо запустить и войти в контейнер,полная последовательность комманд:
```
docker-compose up -d
docker exec -it autorepair_web_1 bash -c "pytest diagnostics/tests ; pytest authorization/tests "
```
# Доступные url и методы:

## Регистрация
### http://localhost/user/register/
##### method: POST
request Data:
```
{
"username":"username",
"password":"SomePassword2",
"password2":"SomePassword2"
}
```
## Авторизация
### http://localhost/user/auth/
##### method: POST
request Data:
```
{
"username":"username",
"password":"SomePassword2",
}
```
response Data:
**"code":200**
data:
```
{
"refresh": "SomeL0ongToke2n",
"access": "SomeLongToke2n"

}
```
**"code":401**
data:
```
{
"detail": "No active account found with the given credentials"
}
```
Используйте access токен для авторизации
request Header:
```
"Authorization" : "Bearer SomeLongToke2n"
```

## Изменение информации о себе
### http://localhost/user/update/
#### * Необходимо авторизоваться
Возможна частичная передача данных
##### method: PUT
 request :

```
{
"last_name":"Testman",
"first_name":"Test",
"middle_name":"Tester"
"auto_mark":"Audi"
}
```
response:
**"code":201**
data:
```
{
"username": "username",
"last_name":"Testman",
"first_name":"Test",
"middle_name":"Tester",
"auto_mark":"Audi"
}
```
**"code":400**
data:
```
{
"last_name": {
"first_name": "field must contain characters only"
}
}
```


## Запись на диагностику
### http:// localhost/diagnostics/
Список специалистов:
```
[
    ('motor', 'Мастер по моторам'),
    ('universal', 'Мастер по общим работам'),
    ('suspension', 'Мастер по обслуживанию подвески'),
    ('transmission', 'Мастер по кпп'),
    ]
 ```
##### method: POST
 request Data:
```
{"time":"2022-02-14 19:00",
"specialist":"suspension"
}
```
response:
**"code":200**
```
{
"id": 1,
"time": "2022-02-14T19:00:00Z",
"specialist": "suspension",
"client": 1
}
```
**"code":400**
```
{
"time": [
"This time for this specialist is busy"
]
}
```
## Список записей
### http://localhost/diagnostics/
##### method: GET
response:
**"code":200**
```
[
{
"id": 1,
"time": "2022-02-14T19:00:00Z",
"specialist": "suspension",
"client": 1
}
]
```
## Админка
### http://localhost/admin
