from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Transaction, AccountKGS, AccountUSD, AccountRUB, AccountEUR


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ['user']

    def validate_amount(self, value):
        if value <= 0:
            raise ValidationError('Введенная сумма не должна быть, отрицательным числом или 0')
        return value

    def validate(self, attrs):
        if attrs['from_currency'] == attrs['to_currency']:
            raise ValidationError('Нельзя менять одну и ту-же валюту')
        return attrs


class AccountKGSSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountKGS
        read_only_fields = ['user', 'code_currency', 'amount']


class AccountUSDSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountUSD
        fields = ('user', 'code_currency', 'amount')
        read_only_fields = ['user', 'code_currency', 'amount']


class AccountEURSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountEUR
        fields = ('user', 'code_currency', 'amount')
        read_only_fields = ['user', 'code_currency', 'amount']


class AccountRUBSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountRUB
        fields = ('user', 'code_currency', 'amount')
        read_only_fields = ['user', 'code_currency', 'amount']
