from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import RegisterSerializer,LoginSerializer ,ProfileSerializer , ChangePasswordSerializer,SendResetPassSerializer,ResetPasswordSerializer
from .models import User
from django.contrib.auth import authenticate
from .renderers import UserRernderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated


#Creating tokens manually

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class RegistrationView(APIView):
    def post(self,request):
        serializer = RegisterSerializer(data = request.data)
        serializer.is_valid(raise_exception=True )
        user = serializer.save()
        token = get_tokens_for_user(user)
        return Response({'mes':'this user is created...   !' ,'token':token} ,  status=status.HTTP_201_CREATED)
        

class LoginView(APIView):
    renderer_classes = [UserRernderer]
    def post(self,request):
        serializer = LoginSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(email = email, password = password)
        if user is not None:
            token=get_tokens_for_user(user)
            return Response({'mes':'login successes fully','token':token},status=status.HTTP_200_OK)
        else:
            return Response({'errors':{'non_field_errors':['Email or Password is not valid']}},status=status.HTTP_400_BAD_REQUEST)
                
    
class ProfileView(APIView):
    renderer_classes=[UserRernderer]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data)
    
class ChangePasswordView(APIView):
    renderer_classes = [UserRernderer]
    permission_classes = [IsAuthenticated]
    def post(self , request):
        serializer = ChangePasswordSerializer(data = request.data , context ={'user': request.user})
        serializer.is_valid(raise_exception=True)
        return Response('Password change success fully',status=status.HTTP_201_CREATED)
    
class SendResetPasswordView(APIView):
    renderer_classes = [UserRernderer]
    def post(self , request):
        serializer = SendResetPassSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        return Response('Password reset link send. please check your email',status=status.HTTP_200_OK)



class ResetPasswordView(APIView):
    def post(self , request, uid , token ):
        serializer = ResetPasswordSerializer(data = request.data , context = {'uid':uid , 'token':token})
        serializer.is_valid(raise_exception=True)
        return Response('Password Reset Successfully...!', status=status.HTTP_200_OK)

