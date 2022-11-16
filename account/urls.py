
from django.urls import path,include
from  account.views import UserRegistrationView,UserLoginView,LogoutAPIView

urlpatterns = [
        path('register/', UserRegistrationView.as_view(),name='register'),
    path('login/', UserLoginView.as_view(),name='login'),
    path('logout/', LogoutAPIView.as_view(), name="logout")
]
