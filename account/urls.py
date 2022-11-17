
from django.urls import path,include
from  account.views import RegisterView,LoginAPIView,LogoutAPIView,VerifyEmail

urlpatterns = [
    path('register/',RegisterView.as_view(),name='register'),
    path('email-verify/', VerifyEmail.as_view(),name='email-verify'),
    path('login/', LoginAPIView.as_view(),name='login'),
    path('logout/', LogoutAPIView.as_view(), name="logout")
]

