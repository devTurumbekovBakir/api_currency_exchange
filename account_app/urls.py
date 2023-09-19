from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from allauth.account.views import ConfirmEmailView

router = DefaultRouter()
router.register('register', views.UserViewSet)
router.register('status', views.StatusUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('accounts/', include('allauth.urls')),
    path('accounts/confirm-email/<str:key>/', ConfirmEmailView.as_view()),
]
