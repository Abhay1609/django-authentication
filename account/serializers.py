from rest_framework import serializers
from account.models import User
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
class UserRegistrationSerializer(serializers.ModelSerializer):
    #we ae writing password2 beacuse password confirmation is also required
    password2=serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model=User
        fields=['roll_no','email','full_name','branch','year','gender','mobile_number','password','password2']
        extra_kwargs={
            'password':{'write_only':True}
        }
    #validating password and confirm password
    def validate(self,attrs):
        password = attrs.get('password')
        password2=attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Passwords are not matching")
        return attrs
    def create(self,validate_data):
        return User.objects.create_user(**validate_data)
class UserLoginSerializer(serializers.ModelSerializer):
    roll_no=serializers.CharField(max_length=14)
    class Meta:
        model=User
        fields=['roll_no','password'] 
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','roll_no','email','full_name']

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    

    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self,attrs):
        self.token= attrs['refresh']
        return attrs


    def save(self,**kwargs):
        try:
            RefreshToken(self.token).blacklist()
        
        except TokenError:
            self.fail('bad_token')
