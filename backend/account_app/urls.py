from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('register', views.UserViewSet)
router.register('status', views.StatusUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('otp/', views.EmailConfirmationView.as_view())
]
