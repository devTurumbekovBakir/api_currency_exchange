from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from .business_logic.currency import get_currency_api
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

            amount = serializer.validated_data['amount']
            from_currency = serializer.validated_data['from_currency']
            to_currency = serializer.validated_data['to_currency']

            user = request.user
            user_discount = user.status.discount
            total_sum = amount * user_discount / 100

            if acc_usd.code_currency == from_currency.upper():
                acc_usd.amount = acc_usd.amount - total_sum
                acc_usd.save()
            elif acc_eur.code_currency == from_currency.upper():
                acc_eur.amount = acc_eur.amount - total_sum
                acc_eur.save()
            elif acc_kgs.code_currency == from_currency.upper():
                acc_kgs.amount = acc_kgs.amount - total_sum
                acc_kgs.save()
            elif acc_rub.code_currency == from_currency.upper():
                acc_rub.amount = acc_rub.amount - total_sum
                acc_rub.save()

            rate = get_currency_api(from_currency, to_currency)
            result = rate * amount


            if acc_usd.code_currency == to_currency.upper():
                acc_usd.amount = acc_usd.amount + result
                acc_usd.save()
            elif acc_eur.code_currency == to_currency.upper():
                acc_eur.amount = acc_eur.amount + result
                acc_eur.save()
            elif acc_kgs.code_currency == to_currency.upper():
                acc_kgs.amount = acc_kgs.amount + result
                acc_kgs.save()
            elif acc_rub.code_currency == to_currency.upper():
                acc_rub.amount = acc_rub.amount + result
                acc_rub.save()

            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
