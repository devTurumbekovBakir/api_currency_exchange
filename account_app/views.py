from rest_framework import status
from rest_framework.authentication import TokenAuthentication

from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.viewsets import ModelViewSet

from .models import User, StatusUser, ConfirmationCode
from .serializers import UserSerializer, StatusUserSerializer
from .permissions import IsStaffUser


class UserViewSet(ModelViewSet):
    queryset = User.objects.all().select_related('statususer')
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]

    def get_permissions(self):
        if self.action == 'list' and not self.request.user.is_staff:
            return [IsStaffUser()]
        elif self.action == 'create':
            return []
        return super().get_permissions()


class StatusUserViewSet(ModelViewSet):
    queryset = StatusUser.objects.all()
    serializer_class = StatusUserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsStaffUser]



class EmailConfirmationView(APIView):
    def post(self, request):
        code = request.data.get('code')
        try:
            confirmation_code = ConfirmationCode.objects.get(code=code)
        except ConfirmationCode.DoesNotExist:
            return Response({'message': 'Неверный код подтверждения.'}, status=status.HTTP_400_BAD_REQUEST)

        user = confirmation_code.user
        user.is_active = True
        user.save()
        return Response({'message': 'Email успешно подтвержден.'}, status=status.HTTP_200_OK)
