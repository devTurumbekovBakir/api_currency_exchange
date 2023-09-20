from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Transaction, AccountKGS, AccountUSD, AccountRUB, AccountEUR


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ['user']

    def validate_amount(self, value):
        if value < 0:
            raise ValidationError('Введенная сумма не должна быть, отрицательным числом')
        return value


class AccountKGSSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountKGS
        fields = '__all__'
        read_only_fields = ['user', 'code_currency']


class AccountUSDSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountUSD
        fields = '__all__'
        read_only_fields = ['user', 'code_currency']


class AccountEURSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountEUR
        fields = '__all__'
        read_only_fields = ['user', 'code_currency']


class AccountRUBSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountRUB
        fields = '__all__'
        read_only_fields = ['user', 'code_currency']
