from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication

from .business_logic.currency import get_currency_api
from .business_logic.transaction import withdraw_from_account, account_replenishment
from .models import Transaction, AccountKGS, AccountUSD, AccountRUB, AccountEUR
from . import serializers


class TransactionListCreateApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        transactions = Transaction.objects.filter(user=request.user).select_related('user')
        serializer = serializers.TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = serializers.TransactionSerializer(data=request.data)
        if serializer.is_valid():

            lists_account = [
                AccountKGS.objects.get(user=request.user),
                AccountUSD.objects.get(user=request.user),
                AccountRUB.objects.get(user=request.user),
                AccountEUR.objects.get(user=request.user)
            ]

            amount = serializer.validated_data['amount']
            from_currency = serializer.validated_data['from_currency'].upper()
            to_currency = serializer.validated_data['to_currency'].upper()

            user_discount = request.user.status.discount

            rate = get_currency_api(from_currency, to_currency)
            result = rate * amount

            for account in lists_account:
                withdraw_from_account(account, from_currency, amount)
                account_replenishment(account, to_currency, result, user_discount)

            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyAccountsList(ListAPIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        acc_kgs = AccountKGS.objects.get(user=request.user).amount
        acc_usd = AccountUSD.objects.get(user=request.user).amount
        acc_rub = AccountRUB.objects.get(user=request.user).amount
        acc_eur = AccountEUR.objects.get(user=request.user).amount
        data = {
            'KGS': acc_kgs,
            'USD': acc_usd,
            'RUB': acc_rub,
            'EUR': acc_eur
        }

        return Response(data)


class UserAccountList(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        acc_kgs = AccountKGS.objects.get(user=request.user).amount
        acc_usd = AccountUSD.objects.get(user=request.user).amount
        acc_rub = AccountRUB.objects.get(user=request.user).amount
        acc_eur = AccountEUR.objects.get(user=request.user).amount
        data = {
            'KGS': acc_kgs,
            'USD': acc_usd,
            'RUB': acc_rub,
            'EUR': acc_eur
        }

        return Response(data)
