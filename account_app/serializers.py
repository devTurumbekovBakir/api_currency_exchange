from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import User, StatusUser
from exchange_app.models import AccountUSD, AccountEUR, AccountRUB, AccountKGS

from allauth.account.models import EmailAddress
from allauth.account.utils import send_email_confirmation


class UserSerializer(serializers.ModelSerializer):
    invest_sum = serializers.FloatField(write_only=True)
    password = serializers.CharField(write_only=True)
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'invest_sum', 'password', 'passport_id', 'status']

    def create(self, validated_data):
        invest_sum = float(validated_data.pop('invest_sum'))
        passport_id = validated_data.get('passport_id')

        if passport_id:
            status = StatusUser.objects.get(number=1)
        elif passport_id is None and invest_sum >= 1000000:
            status = StatusUser.objects.get(number=3)
        else:
            status = StatusUser.objects.get(number=2)

        user = User(username=validated_data['username'], email=validated_data['email'],
                    passport_id=passport_id, status=status)
        user.set_password(validated_data['password'])
        user.save()

        email_address = EmailAddress.objects.create(user=user, email=user.email, primary=True, verified=False)

        AccountUSD.objects.create(user=user, amount=0)
        AccountRUB.objects.create(user=user, amount=0)
        AccountEUR.objects.create(user=user, amount=0)
        AccountKGS.objects.create(user=user, amount=invest_sum)

        send_email_confirmation(self.context['request'], email_address.user)

        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.passport_id = validated_data.get('passport_id', instance.passport_id)

        password = validated_data.get('password')
        if password:
            instance.password = make_password(password)  # хэширование

        instance.save()

        invest_sum = float(validated_data.get('invest_sum', instance.accountsom.amount))

        if instance.passport_id:
            instance.status = StatusUser.objects.get(number=1)
        elif invest_sum >= 100000000:
            instance.status = StatusUser.objects.get(number=3)
        else:
            instance.status = StatusUser.objects.get(number=2)

        instance.accountsom.amount = invest_sum
        instance.accountsom.save()
        instance.save()

        return instance

    def validate_invest_sum(self, value):
        if value < 1000:
            raise ValidationError('Введенная сумма не должна быть меньше 1000 сом')
        return value


class StatusUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusUser
        fields = '__all__'
        read_only_fields = ['user']
