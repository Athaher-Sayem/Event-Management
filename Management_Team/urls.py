from django.urls import path
from .views import SignUpView, LogInView, LogOutView, activate_account

urlpatterns = [
    path('sign-up/', SignUpView, name='sign-up'),
    path('login/', LogInView, name='login'),
    path('logout/', LogOutView, name='logout'),
    path('activate/<str:uidb64>/<str:token>/', activate_account, name='activate_account'),
]
