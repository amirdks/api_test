import json

import jwt
from django.http import HttpRequest
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError
from mail_templated import EmailMessage
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.conf import settings
from accounts.api.utils import EmailThread, get_tokens_for_user
from accounts.api.v1.permissions import IsVerified
from accounts.api.v1.serializers import (
    RegistrationSerializer,
    CustomAuthTokenSerializer,
    CustomTokenObtainPairSerializer,
    ChangePasswordSerializer,
    EmailActivationResendSerializer,
)
from accounts.models import User
from accounts.tasks import send_email_task


class RegistrationAPIView(GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, reqeust: HttpRequest):
        serializer = self.serializer_class(data=reqeust.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        email = serializer.validated_data.get("email")
        data = {"email": email}
        user = get_object_or_404(User, email=email)
        token = get_tokens_for_user(user)
        email_obj = EmailMessage(
            "email/activation_email.tpl",
            {"token": token},
            settings.EMAIL_HOST_USER,
            to=[email],
        )
        EmailThread(email_obj).start()
        return Response(data, status=status.HTTP_201_CREATED)


class CustomObtainAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer
    permission_classes = [IsVerified]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user_id": user.pk, "email": user.email})


class CustomDiscardAuthToken(APIView):
    permission_classes = [IsAuthenticated, IsVerified]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    # permission_classes = [IsVerified]


class ChangePasswordAPIView(GenericAPIView):
    model = User
    permission_classes = [IsAuthenticated, IsVerified]
    serializer_class = ChangePasswordSerializer

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(
                {"details": "password changed successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TestEmailAPIView(APIView):
    def post(self, request):
        # email_obj = EmailMessage(
        #     "email/activation_email.tpl",
        #     {"user": "amir"},
        #     settings.EMAIL_HOST_USER,
        #     to=["amirdks84@gmail.com"],
        # )
        obj = {
            'template_name': 'email/activation_email.tpl',
            'context': {"user": "amir"},
            'args': settings.EMAIL_HOST_USER,
            'to': ["amirdks84@gmail.com"]
        }
        # EmailThread(email_obj).start()
        send_email_task.apply_async(args=[obj])
        return Response({"detail": "email sent"}, status=status.HTTP_200_OK)


class EmailActivationAPIView(APIView):
    def get(self, request, token, *args, **kwargs):
        try:
            token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = token.get("user_id")
        except ExpiredSignatureError:
            return Response(
                {"detail": "token has been expired"}, status=status.HTTP_400_BAD_REQUEST
            )
        except InvalidSignatureError:
            return Response(
                {"detail": "token is invalid"}, status=status.HTTP_400_BAD_REQUEST
            )
        user = get_object_or_404(User, id=user_id)
        if user.is_verified:
            return Response(
                {"detail": "user is already verified"}, status=status.HTTP_200_OK
            )
        user.is_verified = True
        user.save()
        return Response(
            {"detail": "user verified successfully"}, status=status.HTTP_200_OK
        )


class EmailActivationResendAPIView(GenericAPIView):
    serializer_class = EmailActivationResendSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get("user")
        user = get_object_or_404(User, email=user.email)
        token = get_tokens_for_user(user)
        email_obj = EmailMessage(
            "email/activation_email.tpl",
            {"token": token},
            settings.EMAIL_HOST_USER,
            to=[user.email],
        )
        EmailThread(email_obj).start()
        return Response({"detail": "email resent"}, status=status.HTTP_200_OK)
