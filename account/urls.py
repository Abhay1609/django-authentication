
from django.urls import path,include
from  account.views import UserRegistrationView,UserLoginView,LogoutAPIView,VerifyEmail,PasswordTokenCheckAPI,RequestPasswordRestEmail,SetNewPasswordAPIView

urlpatterns = [
        path('register/', UserRegistrationView.as_view(),name='register'),
        path('email-verify/', VerifyEmail.as_view(),name='email-verify'),
    path('login/', UserLoginView.as_view(),name='login'),
    path('logout/', LogoutAPIView.as_view(), name="logout"),
    path('request-reset-email/',RequestPasswordRestEmail.as_view(),name="request-reset-email"),
    path('password-reset/<uidb64>/<token>/',PasswordTokenCheckAPI.as_view(),name='password-reset'),
    path('password-reset-complete',SetNewPasswordAPIView.as_view(),name='password-reset-complete')
]
