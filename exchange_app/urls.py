from django.urls import path

from . import views

urlpatterns = [
    path('', views.TransactionListCreateApiView.as_view())
]
