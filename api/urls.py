# from django.conf.urls import url
from django.urls import include, re_path

from django.urls import path, include
from .views import ( 
    CustomAuthToken,
    ListUsers,
    WalletApiView,
    DepositApiView,
    WithdrawApiView
)

urlpatterns = [
    path('users/', ListUsers.as_view()),
    path('init', CustomAuthToken.as_view()),
    path('wallet', WalletApiView.as_view()),
    path('deposits', DepositApiView.as_view()),
    path('withdrawals', WithdrawApiView.as_view()),
 
]
