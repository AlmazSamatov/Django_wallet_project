from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models import ForeignKey
from djmoney.models.fields import MoneyField


class Wallet(models.Model):
    user = ForeignKey(User, on_delete=models.DO_NOTHING)
    amount_of_rub = MoneyField(max_digits=10, decimal_places=2, default=0, default_currency='RUB')
    amount_of_usd = MoneyField(max_digits=10, decimal_places=2, default=0, default_currency='USD')
    amount_of_euro = MoneyField(max_digits=10, decimal_places=2, default=0, default_currency='EUR')
