from django.shortcuts import render
from .models import Profile
from .serializer import *
from rest_framework import viewsets
from rest_framework.status import *
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

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






