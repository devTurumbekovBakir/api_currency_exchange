from django.urls import path

from . import views

urlpatterns = [
    path('api/change/', views.TransactionListCreateApiView.as_view()),
    path('api/company/accounts/', views.CompanyAccounts.as_view())
]
