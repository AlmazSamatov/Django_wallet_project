from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from djangoProject.djangoProject.models import Wallet


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        wallet = Wallet(user=user)
        wallet.save()
        Token.objects.create(user=user)
        return user


class WalletSerializer(serializers.ModelSerializer):
    username = serializers.RelatedField(source='User', read_only=True)

    class Meta:
        model = Wallet
        fields = ('username', 'amount_of_rub', 'amount_of_usd', 'amount_of_euro')
