from django.urls import path

from . import views

urlpatterns = [
    path('api/change/', views.TransactionListCreateApiView.as_view()),
    path('api/company/accounts/', views.CompanyAccountsList.as_view()),
    path('api/user/accounts/', views.UserAccountList.as_view())
]
