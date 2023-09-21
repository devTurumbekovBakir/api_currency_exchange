import random
import string

from django.core.mail import send_mail
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import User, StatusUser, ConfirmationCode
from exchange_app.models import AccountUSD, AccountEUR, AccountRUB, AccountKGS


class UserSerializer(serializers.ModelSerializer):
    invest_sum = serializers.FloatField(write_only=True)
    password = serializers.CharField(write_only=True)
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = User

        fields = ['id', 'username', 'email', 'invest_sum', 'password', 'passport_id']

    def create(self, validated_data):
        invest_sum = float(validated_data.pop('invest_sum'))
        passport_id = validated_data.get('passport_id')
        username = validated_data['username']

        if username.startswith('admin'):
            is_staff = True
            account_amount = 0
            status = None
        else:
            is_staff = False
            account_amount = invest_sum

            if passport_id:
                status = StatusUser.objects.get(number=1)
            elif passport_id is None and invest_sum >= 1000000:
                status = StatusUser.objects.get(number=3)
            else:
                status = StatusUser.objects.get(number=2)

        user = User(username=validated_data['username'], email=validated_data['email'],
                    passport_id=passport_id, status=status, is_active=False, is_staff=is_staff)

        user.set_password(validated_data['password'])
        user.save()

        AccountUSD.objects.create(user=user, amount=0)
        AccountRUB.objects.create(user=user, amount=0)
        AccountEUR.objects.create(user=user, amount=0)
        AccountKGS.objects.create(user=user, amount=account_amount)

        code = ''.join(random.choices(string.digits, k=6))
        ConfirmationCode.objects.create(user=user, code=code)

        send_mail(
            'Код подтверждения',
            f'Ваш код подтверждения: {code}',
            'bakirturumbekov37@gmail.com',
            [user.email],
            fail_silently=False,
        )

        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.passport_id = validated_data.get('passport_id', instance.passport_id)

        password = validated_data.get('password')
        if password:
            instance.set_password(password)

        if instance.passport_id:
            instance.status = StatusUser.objects.get(number=1)

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


class EmailConfirmationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfirmationCode
        fields = ['code']
