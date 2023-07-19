from django.shortcuts import render
from .models import Profile
from .serializer import *
from rest_framework import viewsets
from rest_framework.status import *
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from .emails import send_via_mail


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class Profile_Register(viewsets.ViewSet):

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            sr = Profile_serializer(data=data)
            if sr.is_valid():
                user = sr.save()
                token = get_tokens_for_user(user)
                return Response({'msg': token}, status=HTTP_201_CREATED)
            return Response(sr.errors, status=HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)
            return Response(
                {'msg':'something went wrong '},

            )

class LoginViewset(viewsets.ViewSet):

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            sr = LoginSerializer(data=data)
            if not sr.is_valid():
                return Response({'msg': sr.errors},
                                status=HTTP_400_BAD_REQUEST)
            responce = sr.get_jwt_token(sr.data)
            return Response(responce, status=HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'msg':'something went wrong '},status=HTTP_400_BAD_REQUEST)

class LogOutViewset(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            refresh = data['RefreshToken']
            token = RefreshToken(refresh)
            token.blacklist()
            if not token:
                return Response({'msg':'wrong token'},status=HTTP_400_BAD_REQUEST)
            return Response({'msg':'logout successfully...'},status=HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'msg':'something went wrong.'},status=HTTP_400_BAD_REQUEST)


class ForgotPasswordViewset(viewsets.ViewSet):
    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            if data.get('email') is None:
                return Response({'msg':'email is required...'},status=HTTP_400_BAD_REQUEST)
            sr = ForgotPasswordSerializer(data=data)
            if not sr.is_valid():
                return Response(sr.errors,status=HTTP_400_BAD_REQUEST)
            send_via_mail(sr.validated_data['email'])
            return Response({'msg':'otp sent on email ..'},status=HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'msg':'something went wrong '},status=HTTP_400_BAD_REQUEST)

class verifyOtpView(viewsets.ViewSet):

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            if data.get('email') is None:
                return Response({'msg': 'email is required..'}, status=HTTP_400_BAD_REQUEST)
            user = Profile.objects.get(email=data.get('email'))
            if user.otp != data.get('otp'):
                return Response({'msg': 'wrong otp  ...'}, status=HTTP_400_BAD_REQUEST)
            if user.otp == data.get('otp'):
                return Response({'msg': 'otp is macthed'}, status=HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'msg':'something went wrong ...'},status=HTTP_400_BAD_REQUEST)



class NewPassword(viewsets.ViewSet):
    def create(self, request, *args, **kwargs):
        try:
            data = request.data

            if data['password'] is None:
                return Response({'password is required'},status=HTTP_400_BAD_REQUEST)

            if data['confirm_password'] is None:
                return Response({'msg':'confirm password is required'},status=HTTP_400_BAD_REQUEST)

            if  data['password'] != data['confirm_password'] :
                return Response({'msg':'password and confirm password should be same '})

            user = Profile.objects.get(email__exact= data['email'])
            user.password = data.get('password')
            user.confirm_password = data.get('confirm_password')
            user.save()
            return Response({'msg':'password is changed '},status=HTTP_201_CREATED)

        except Exception as e:
            print(e)
            return Response({'msg':'something went wrong'},status=HTTP_400_BAD_REQUEST)



























