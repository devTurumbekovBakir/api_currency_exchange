from rest_framework.authentication import TokenAuthentication
from rest_framework.viewsets import ModelViewSet

from .models import User, StatusUser
from .serializers import UserSerializer, StatusUserSerializer
from .permissions import IsStaffUser


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
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
