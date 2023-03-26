from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenObtainPairView,
    TokenVerifyView,
)

from .. import views

urlpatterns = [
    # registration
    path(
        "registration/",
        views.RegistrationAPIView.as_view(),
        name="registration_api_view",
    ),
    # change password
    path(
        "password-change",
        views.ChangePasswordAPIView.as_view(),
        name="change_password_api",
    ),
    # login token
    path("token/login/", views.CustomObtainAuthToken.as_view(), name="token_login_api"),
    path(
        "token/logout/", views.CustomDiscardAuthToken.as_view(), name="token_logout_api"
    ),
    # jwt
    path(
        "jwt/create/",
        views.CustomTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="token_verify"),
    # email send
    path("test-email", views.TestEmailAPIView.as_view(), name="test_email"),
    path(
        "activation/confirm/<str:token>",
        views.EmailActivationAPIView.as_view(),
        name="email_activation_api",
    ),
    path(
        "activation/resend/",
        views.EmailActivationResendAPIView.as_view(),
        name="email_activation_resend_api",
    ),
]
