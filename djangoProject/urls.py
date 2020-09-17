"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from rest_framework.authtoken.views import obtain_auth_token

from djangoProject.djangoProject.views import UserCreate, add_money, watch_wallet, withdraw_money, send_money, \
    convert_money

urlpatterns = [
    path('admin/', admin.site.urls),
    path("login/", obtain_auth_token, name="login"),
    path("user_create/", UserCreate.as_view(), name="user_create"),
    path("add_money/", add_money, name="add_money"),
    path("withdraw_money/", withdraw_money, name="withdraw_money"),
    path("watch_wallet/", watch_wallet, name="watch_wallet"),
    path("send_money/", send_money, name="send_money"),
    path("convert_money/", convert_money, name="convert_money")
]
