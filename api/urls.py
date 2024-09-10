from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView,TokenVerifyView
from .views import RegistrationView,LoginView,ProfileView,ChangePasswordView,SendResetPasswordView,ResetPasswordView
urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(),name='token_refresh_pair'),
    path('api/token/verify/', TokenVerifyView.as_view(),name='token_verify_pair'),
    path('register/',RegistrationView.as_view()),
    path('login/',LoginView.as_view()),
    path('profile/',ProfileView.as_view()),
    path('changepassword/',ChangePasswordView.as_view()),
    path('send-reset-password/',SendResetPasswordView.as_view()),
    path('reset-password/<uid>/<token>/',ResetPasswordView.as_view()),
]
