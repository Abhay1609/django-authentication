from rest_framework.response import Response
from rest_framework import status,generic,permissions
from rest_framework.views import APIView
from account.serializers import UserRegistrationSerializer,UserLoginSerializer,UserProfileSerializer,LogoutSerializer
from account.renderers import UserRenderer
from django.contrib.auth import authenticate  
from rest_framework_simplejwt.tokens import RefreshToken 
from rest_framework.permissions import IsAuthenticated 

def get_tokens_for_user(user):
    refresh=RefreshToken.for_user(user)

    return {
        'refresh':str(refresh),
        'access':str(refresh.access_token)
    }

class UserRegistrationView(APIView):
    renderer_classes=[UserRenderer] 
    def post(self,request,format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
            token=get_tokens_for_user(user)
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
                token=get_tokens_for_user(user)
                return Response({'token':token,'msg':'Login Succesful'},status=status.HTTP_200_OK)
            else:
                return Response({'errors':{'non_field_errors':['Username or Password is incorrect']}},status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(generic.GenericAPIView):
    serializer_class=LogoutSerializer

    permission_classes = (permissions.IsAuthenticated,)

    def post(self,request):
        serializer= self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()


        return Response(status=status.HTTP_204_NO_CONTENT)