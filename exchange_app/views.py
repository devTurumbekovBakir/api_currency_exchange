from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from .business_logic.currency import get_currency_api
from .business_logic.transaction import withdraw_from_account, account_replenishment
from .models import Transaction, AccountKGS, AccountUSD, AccountRUB, AccountEUR
from .serializers import TransactionSerializer


class TransactionListCreateApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        transactions = Transaction.objects.all()
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():

            acc_kgs = AccountKGS.objects.get(user=request.user)
            acc_usd = AccountUSD.objects.get(user=request.user)
            acc_rub = AccountRUB.objects.get(user=request.user)
            acc_eur = AccountEUR.objects.get(user=request.user)

            lists_account = [acc_eur, acc_rub, acc_usd, acc_kgs]

            amount = serializer.validated_data['amount']
            from_currency = serializer.validated_data['from_currency']
            to_currency = serializer.validated_data['to_currency']

            user = request.user
            user_discount = user.status.discount

            rate = get_currency_api(from_currency, to_currency)
            result = rate * amount

            discount = amount * user_discount / 100
            amount += discount

            for account in lists_account:
                withdraw_from_account(account, from_currency, amount)
                account_replenishment(account, to_currency, result)

            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
