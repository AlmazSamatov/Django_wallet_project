# Create your views here.
from djmoney.money import Money
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User

from djangoProject.djangoProject.models import Wallet
from djangoProject.djangoProject.serializers import UserSerializer, WalletSerializer


class UserCreate(generics.CreateAPIView):
    http_method_names = ['post', 'head']
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_money(request):
    """
        money_amount -- Amount of money to add
        currency -- Currency (RUB, USD, EUR)
    """
    money_amount = float(request.data.get("money_amount"))
    currency = str(request.data.get("currency")).lower()
    if currency not in ['rub', 'usd', 'eur']:
        return Response({"error": "Wrong currency"}, status=status.HTTP_400_BAD_REQUEST)
    elif money_amount < 0:
        return Response({"error": "Negative amount of money"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        username = request.user.username
        wallet = Wallet.objects.get(user__username=username)
        if currency == 'rub':
            wallet.amount_of_rub += Money(money_amount, 'RUB')
        elif currency == 'usd':
            wallet.amount_of_usd += Money(money_amount, 'USD')
        elif currency == 'eur':
            wallet.amount_of_euro += Money(money_amount, 'EUR')
        wallet.save()
    return Response({"status": "{} {} added to your wallet".format(money_amount, currency)}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_money(request):
    """
        username -- A user to whom you want to send money
        money_amount -- Amount of money to send
        currency -- Currency (RUB, USD, EUR)
    """
    another_username = str(request.data.get("username"))
    money_amount = float(request.data.get("money_amount"))
    currency = str(request.data.get("currency")).lower()
    if currency not in ['rub', 'usd', 'eur']:
        return Response({"error": "Wrong currency"}, status=status.HTTP_400_BAD_REQUEST)
    elif money_amount < 0:
        return Response({"error": "Negative amount of money"}, status=status.HTTP_400_BAD_REQUEST)
    elif not User.objects.filter(username=another_username).exists():
        return Response({"error": "User with username: {} does not exit".format(another_username)},
                        status=status.HTTP_400_BAD_REQUEST)
    else:
        self_username = request.user.username
        self_wallet = Wallet.objects.get(user__username=self_username)
        another_wallet = Wallet.objects.get(user__username=another_username)
        if currency == 'rub':
            money_amount_in_cur = Money(money_amount, 'RUB')
            if self_wallet.amount_of_rub < money_amount_in_cur:
                return Response({"error": "You dont have enough money in your wallet of this currency"},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                self_wallet.amount_of_rub -= money_amount_in_cur
                another_wallet.amount_of_rub += money_amount_in_cur
        elif currency == 'usd':
            money_amount_in_cur = Money(money_amount, 'USD')
            if self_wallet.amount_of_usd < money_amount_in_cur:
                return Response({"error": "You dont have enough money in your wallet of this currency"},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                self_wallet.amount_of_usd -= money_amount_in_cur
                another_wallet.amount_of_usd += money_amount_in_cur
        elif currency == 'eur':
            money_amount_in_cur = Money(money_amount, 'EUR')
            if self_wallet.amount_of_euro < money_amount_in_cur:
                return Response({"error": "You dont have enough money in your wallet of this currency"},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                self_wallet.amount_of_euro -= money_amount_in_cur
                another_wallet.amount_of_euro += money_amount_in_cur
        self_wallet.save()
        another_wallet.save()
    return Response({"status": "{} {} sent to user {} wallet".format(money_amount, currency, another_username)},
                    status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def withdraw_money(request):
    """
        money_amount -- Amount of money to witdraw
        currency -- Currency (RUB, USD, EUR)
    """
    money_amount = float(request.data.get("money_amount"))
    currency = str(request.data.get("currency")).lower()
    if currency not in ['rub', 'usd', 'eur']:
        return Response({"error": "Wrong currency"}, status=status.HTTP_400_BAD_REQUEST)
    elif money_amount < 0:
        return Response({"error": "Negative amount of money"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        username = request.user.username
        wallet = Wallet.objects.get(user__username=username)
        if currency == 'rub':
            money_amount_in_cur = Money(money_amount, 'RUB')
            if wallet.amount_of_rub < money_amount_in_cur:
                return Response({"error": "You dont have enough money in your wallet of this currency"},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                wallet.amount_of_rub -= money_amount_in_cur
        elif currency == 'usd':
            money_amount_in_cur = Money(money_amount, 'USD')
            if wallet.amount_of_rub < money_amount_in_cur:
                return Response({"error": "You dont have enough money in your wallet of this currency"},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                wallet.amount_of_rub -= money_amount_in_cur
        elif currency == 'eur':
            money_amount_in_cur = Money(money_amount, 'EUR')
            if wallet.amount_of_rub < money_amount_in_cur:
                return Response({"error": "You dont have enough money in your wallet of this currency"},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                wallet.amount_of_rub -= money_amount_in_cur
        wallet.save()
    return Response({"status": "{} {} withdrawed from your wallet".format(money_amount, currency)},
                    status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def convert_money(request):
    """
        money_amount -- Amount of money to convert
        currency_from -- Currency from which you want to convert (RUB, USD, EUR)
        currency_to -- Currency to which you want to convert (RUB, USD, EUR)
    """
    money_amount = float(request.data.get("money_amount"))
    currency_from = str(request.data.get("currency_from")).lower()
    currency_to = str(request.data.get("currency_to")).lower()

    if currency_from not in ['rub', 'usd', 'eur']:
        return Response({"error": "Wrong currency_from"}, status=status.HTTP_400_BAD_REQUEST)
    elif currency_to not in ['rub', 'usd', 'eur']:
        return Response({"error": "Wrong currency_to"}, status=status.HTTP_400_BAD_REQUEST)
    elif money_amount < 0:
        return Response({"error": "Negative amount of money"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        username = request.user.username
        wallet = Wallet.objects.get(user__username=username)
        if currency_from == 'rub':
            money_amount_in_cur = Money(money_amount, 'RUB')
            if wallet.amount_of_rub < money_amount_in_cur:
                return Response({"error": "You dont have enough money in your wallet of this currency"},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                wallet.amount_of_rub -= money_amount_in_cur
        elif currency_from == 'usd':
            money_amount_in_cur = Money(money_amount, 'USD')
            if wallet.amount_of_rub < money_amount_in_cur:
                return Response({"error": "You dont have enough money in your wallet of this currency"},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                wallet.amount_of_rub -= money_amount_in_cur
        elif currency_from == 'eur':
            money_amount_in_cur = Money(money_amount, 'EUR')
            if wallet.amount_of_rub < money_amount_in_cur:
                return Response({"error": "You dont have enough money in your wallet of this currency"},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                wallet.amount_of_rub -= money_amount_in_cur

        if currency_to == 'rub':
            wallet.amount_of_rub += money_amount_in_cur
        elif currency_to == 'usd':
            wallet.amount_of_usd += money_amount_in_cur
        elif currency_to == 'eur':
            wallet.amount_of_euro += money_amount_in_cur

        wallet.save()
    return Response({"status": "Converted {} {} from {} wallet to {} wallet".format(money_amount, currency_from,
                                                                                    currency_from, currency_to)},
                    status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def watch_wallet(request):
    username = request.user.username
    wallet = Wallet.objects.get(user__username=username)
    serializer = WalletSerializer(wallet)
    return Response(serializer.data)
