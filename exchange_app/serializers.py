from rest_framework import serializers

from .models import Transaction, AccountKGS, AccountUSD, AccountRUB, AccountEUR


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ['user']


class AccountKGSSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountKGS
        fields = '__all__'
        read_only_fields = ['user']


class AccountUSDSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountUSD
        fields = '__all__'
        read_only_fields = ['user']


class AccountEURSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountEUR
        fields = '__all__'
        read_only_fields = ['user']


class AccountRUBSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountRUB
        fields = '__all__'
        read_only_fields = ['user']
