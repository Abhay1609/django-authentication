
from django.urls import path,include
from  account.views import UserRegistrationView,UserLoginView,LogoutAPIView,verifyEmail

urlpatterns = [
        path('register/', UserRegistrationView.as_view(),name='register'),
        path('email-verify/', verifyEmail.as_view(),name='email-verify'),
    path('login/', UserLoginView.as_view(),name='login'),
    path('logout/', LogoutAPIView.as_view(), name="logout")
]
