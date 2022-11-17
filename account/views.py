from rest_framework.response import Response
from rest_framework import status, generics ,permissions
from rest_framework.views import APIView
from account.serializers import UserRegistrationSerializer,UserLoginSerializer,UserProfileSerializer,LogoutSerializer,EmailVerificationSerializer,ResetPasswordEmailRequestSerializer,SetNewPasswordSerializer
from account.renderers import UserRenderer
from django.contrib.auth import authenticate  
from rest_framework_simplejwt.tokens import RefreshToken 
from rest_framework.permissions import IsAuthenticated 
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .models import User
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi 

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str,force_str,smart_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util


class UserRegistrationView(APIView):
    renderer_classes=[UserRenderer] 
    def post(self,request,format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
            token=str(RefreshToken.for_user(user).access_token)
            current_site=get_current_site(request).domain
            relative_link=reverse('email-verify')
            absurl='http://'+current_site+relative_link+"?token="+ str(token)
            email_body='Hi '+user.full_name +' Use link below to verify your email \n '+ absurl
            data={'email_body':email_body,'to_email':user.email,'email_subject':'Verify your email'}
            Util.send_email(data)
            return Response({'token':token,'msg':'Registartion Successful'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
class UserLoginView(APIView):
    def post(self,request,format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            roll_no=serializer.data.get('roll_no')
            password=serializer.data.get('password')
            user=authenticate(roll_no=roll_no,password=password)
            if user is not None:
                token=RefreshToken.for_user(user) 
                return Response({'token':token,'msg':'Login Succesful'},status=status.HTTP_200_OK)
            else:
                return Response({'errors':{'non_field_errors':['Username or Password is incorrect']}},status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)
class VerifyEmail(APIView):
    serializers_class=EmailVerificationSerializer
    #token_param_config=openapi.Parameter('token',in_=openapi.IN_QUERY)
    #@swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self,request):
        token=request.GET.get('token')
        try:
            payload=jwt.decode(token,settings.SECRET_KEY)
            user=User.objects.get(id=payload['user_id'])
            if not user.isverified:
                user.isverified=True
                user.save()

            return Response({'email':'Successfully activated'},status=status.HTTP_200_OK)
        except  jwt.ExpiredSignatureError as identifier:
            return Response({'error':'Activation Link Expired'},status=status.HTTP_400_BAD_REQUEST)
        except  jwt.exceptions.DecodeError as identifier:
            return Response({'error':'Invalid Token'},status=status.HTTP_400_BAD_REQUEST)
        
            

      
   

class LogoutAPIView(generics.GenericAPIView):
    serializer_class=LogoutSerializer

    permission_classes = (permissions.IsAuthenticated,)

    def post(self,request):
        serializer= self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()


        return Response(status=status.HTTP_204_NO_CONTENT)
class RequestPasswordRestEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer
    def post(self,request):

        serializers=self.serializer_class(data=request.data)
        email = request.data['email']
        if User.objects.filter(email=email).exists():
            user=User.objects.get(email=email)
            uidb64=urlsafe_base64_encode(smart_bytes(user.id))
            token=PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request=request).domain
            relative_link = reverse('password-reset',kwargs={'uidb64':uidb64,'token':token})
            absurl = 'http://' + current_site + relative_link
            email_body = 'Hello Use link below to reset your password \n ' + absurl
            data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'Reset your Password'}
            Util.send_email(data)
        return Response({'sucess':'We have sent you a link of reset password'},status=status.HTTP_200_OK)
class PasswordTokenCheckAPI(generics.GenericAPIView):
    def get(self,request,uidb64,token):
        try:
            id=smart_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(id=id)



            if not PasswordResetTokenGenerator().check_token(user,token):
                return Response({'error':'Token is not valid request for new one'},status=status.HTTP_401_UNAUTHORIZED)
            return Response({'success': True, 'message': 'creadentials Valid', 'uidb64': uidb64, 'token': token},status=status.HTTP_200_OK)
        except DjangoUnicodeDecodeError as identifier:
            if not PasswordResetTokenGenerator().check_token(user):
                return Response({'error':'Token is not  vlaid'},status=status.HTTP_401_UNAUTHORIZED)

class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class=SetNewPasswordSerializer
    def patch(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'sucess':True,'message':'Password reset success'},status=status.HTTP_200_OK)

