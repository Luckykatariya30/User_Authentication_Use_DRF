from rest_framework import serializers
from .models import User
from xml.dom import ValidationErr
from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from .utils import Util

class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'},write_only = True)
    class Meta:
        model = User
        fields = ['name','email','date_of_birth','password','password2']
        extra_kwargs = {
            'password':{'write_only': True}
        }

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password!=password2 :
            raise serializers.ValidationError("Password and Password2 doesn't match")
        return attrs
    def create(self, validate_data):
        return User.objects.create_user(**validate_data)
    

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length = 224)
    class Meta:
        model = User
        fields = ['email','password']
        

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email','name']

class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length = 121 ,style = {'input_type':'password'} , write_only = True)
    password2 = serializers.CharField(max_length = 121, style = {'input_type':'password'} , write_only = True)
    class Meta:
        fields = ['password','password2']


    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("Password and confirm Password doesn't match")
        user.set_password(password)
        user.save()
        return attrs

class SendResetPassSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length = 121)
    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email  = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid  = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            link = 'http://localhost:3000/reset/'+uid+'/'+token
            print("link", link)

            #Send Email
            body = 'Click Following Link to Reset Your Password '+link
            data = {
                'subject' : 'reset your password',
                'body':body,
                'to_email':user.email

            }
            Util.send_email(data)
            return attrs
        else:
            raise ValidationErr('You are not a registered user ....!')
        

class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length = 121 ,style = {'input_type':'password'} , write_only = True)
    password2 = serializers.CharField(max_length = 121, style = {'input_type':'password'} , write_only = True)
    class Meta:
        fields = ['password','password2']


    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')

            if password != password2:
                raise serializers.ValidationError("Password     and confirm Password doesn't match")
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id = id)
            if not PasswordResetTokenGenerator().check_token    (user,token):
                raise ValidationErr('Token is not velid')
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user,token)
            raise ValidationErr('Token is not valid or expired ')

    

    