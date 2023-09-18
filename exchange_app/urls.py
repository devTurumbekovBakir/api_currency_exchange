from django.urls import path

from . import views

urlpatterns = [
    path('change/', views.TransactionListCreateApiView.as_view())
]
