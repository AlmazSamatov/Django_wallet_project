# Django_wallet_project


Для запуска проекта нужен docker.

Команда docker-compose up запускает проект на 8000 порту.

Курс валют обновляется ежедневно в 00:00.

## Методы API:

Не нужен токен аутентификации:

1. user_create/ POST запрос 

JSON:
```
{
    "email": "Adel@gmail.com",
    "username": "Adel",
    "password": "qwerty"
}
```

2. login/ POST запрос

JSON:
```
{
    "username": "Adel",
    "password": "qwerty"
}
```

Нужен токен аутентификации:

3. watch_wallet/ GET запрос 

4. add_money/ POST запрос

JSON:
```
{
    "money_amount": 100,
    "currency": "rub"
}
```

5. withdraw_money/ POST запрос

JSON:
```
{
    "money_amount": 100,
    "currency": "rub"
}
```


6. send_money/ POST запрос

JSON:
```
{
    "username": "Adel",
    "money_amount": 90,
    "currency": "rub"
}
```

7. convert_money/ POST запрос

JSON:
```
{
    "currency_to": "USD",
    "money_amount": 100,
    "currency_from": "rub"
}
```




