from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny
from .models import *
from .serializer import *
from rest_framework.status import *


class ProfileView(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self,request,*args,**kwargs):
        obj = Profile_Page.objects.filter(user=request.user)
        sr = Profile_Page_Serializer(obj,many=True)
        return Response(sr.data,status=HTTP_200_OK)
    def create(self, request, *args, **kwargs):
        data = request.data
        data['user'] = request.user.id
        sr = Profile_Page_Serializer(data=data)
        if not sr.is_valid():
            return Response({'msg':sr.errors},status=HTTP_400_BAD_REQUEST)
        sr.save()
        return Response(sr.data,status=HTTP_201_CREATED)


class PostView(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self,request, *args, **kwargs):
        obj = Posts.objects.filter(user_id = request.user)
        sr = PostSerializer(obj, many=True)
        return Response(sr.data,status=HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            user = request.user

            Posts.objects.create(Profile_id=Profile_Page.objects.get(uuid= data.get('Profile_id'))
                                       ,user_id = Profile.objects.get(username = user),
                                       post = data.get('post'))

            return Response({'msg': 'Post uploded'}, status=HTTP_201_CREATED)

        except Exception as e:
            print(e)
            return Response({'msg':'something went wrong '},status=HTTP_400_BAD_REQUEST)


class POST_LIST(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def list(self,request,*args,**kwargs):
        try:
            obj = Posts.objects.all()
            sr = PostSerializer(obj, many=True)
            return Response(sr.data, status=HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({'msg':'something went wrong '},status=HTTP_400_BAD_REQUEST)



class VideoPostViewset(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            VideoPost.objects.create(
                user_id=request.user,
                Profile_id=Profile_Page.objects.get(uuid=data.get('profile_id')),
                file=data.get('file')
            )
            return Response({'msg': 'video posted..'})
        except Exception as e:
            print(e)
            return Response({'msg':'something went wrong...'})

class HighlightesView(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self,request,*args,**kwargs):
        try:
            data = request.data
            hightlites.objects.create(
                user_id=request.user,
                Profile_id=Profile_id.objects.get(uuid=data.get('Profile_id')),
                stories=data.get('file')
            )
            return Response({'msg': 'stories added ...'},status=HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({'msg':'something went wrong ..'},status=HTTP_400_BAD_REQUEST)













