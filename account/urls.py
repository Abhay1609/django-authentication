
from django.urls import path,include
from  account.views import UserRegistrationView,UserLoginView,LogoutAPIView,VerifyEmail

urlpatterns = [
        path('register/', UserRegistrationView.as_view(),name='register'),
        path('email-verify/', VerifyEmail.as_view(),name='email-verify'),
    path('login/', UserLoginView.as_view(),name='login'),
    path('logout/', LogoutAPIView.as_view(), name="logout")
]
