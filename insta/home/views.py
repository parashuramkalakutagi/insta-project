from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny,IsAuthenticatedOrReadOnly
from .models import *
from .serializer import *
from rest_framework.status import *
from django.db.models import Count
from rest_framework import generics
from rest_framework.mixins import UpdateModelMixin
from rest_framework.generics import GenericAPIView
from rest_framework.filters import SearchFilter
from rest_framework.generics import UpdateAPIView
from  django.db.models import Count,Max,Min,Avg,Sum,SET
from django.db.models import Q , F
from datetime import timedelta
from django.utils import timezone
import datetime

class ProfileView(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]



    def list(self, request, *args, **kwargs):
        obj = Profile_Page.objects.filter(user=request.user).values_list('uuid','name')
        sr = Profile_Page_Serializer(obj, many=True)
        return Response(obj)

    def create(self, request, *args, **kwargs):
        data = request.data
        data['user'] = request.user.id
        sr = Profile_Page_Serializer(data=data)
        if not sr.is_valid():
            return Response({'msg': sr.errors}, status=HTTP_400_BAD_REQUEST)
        sr.save()
        return Response(sr.data, status=HTTP_201_CREATED)



class PostView(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        obj = Posts.objects.filter(user_id=request.user).values_list('Profile_id','post')
        sr = PostSerializer(obj, many=True)
        return Response(sr.data, status=HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            user = request.user

            Posts.objects.create(Profile_id=Profile_Page.objects.get(uuid=data.get('Profile_id'))
                                 , user_id=Profile.objects.get(username=user),
                                 post=data.get('post'))

            return Response({'msg': 'Post uploded'}, status=HTTP_201_CREATED)

        except Exception as e:
            print(e)
            return Response({'msg': 'something went wrong '}, status=HTTP_400_BAD_REQUEST)


class POST_LIST(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        try:
            obj = Posts.objects.all().values_list('Profile_id','post')
            return Response(obj, status=HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({'msg': 'something went wrong '}, status=HTTP_400_BAD_REQUEST)

class PostCountViewset(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def list(self,request):
        try:
            object = Posts.objects.filter(user_id= request.user).values('Profile_id').aggregate(total_posts= Count('post'))
            return Response(object)

        except Exception as e:
            print(e)
            return Response(status=HTTP_400_BAD_REQUEST)

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
            return Response({'msg': 'something went wrong...'})


class HighlightesView(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            hightlites.objects.create(
                user_id=request.user,
                Profile_id=Profile_id.objects.get(uuid=data.get('Profile_id')),
                stories=data.get('file')
            )
            return Response({'msg': 'stories added ...'}, status=HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({'msg': 'something went wrong ..'}, status=HTTP_400_BAD_REQUEST)


class LikeViewset(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            user_id = request.user
            if Likes.objects.filter(user_id=user_id,
                                    profile_id=data.get('profile_id'),
                                    post_id=data.get('post_id')).exists():
                return Response({'msg': 'alredy this user is liked post'}, status=HTTP_400_BAD_REQUEST)

            Likes.objects.create(user_id=Profile.objects.get(username=user_id),
                                 profile_id=Profile_Page.objects.get(uuid=data.get('profile_id')),
                                 post_id=Posts.objects.get(uuid=data.get('post_id')))

            return Response({'msg': ' post is liked'})

        except Exception as e:
            print(e)
            return Response({'msg': 'something went wrong..'}, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        try:

            data = request.data
            unlike = Likes.objects.filter(post_id=data.get('post_id'))
            if not unlike.exists():
                return Response({'msg': 'alredy unliked the post'}, status=HTTP_400_BAD_REQUEST)
            unlike[0].delete()
            return Response({'msg': 'unliked...!'}, status=HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({'msg': 'something went wrong'}, status=HTTP_400_BAD_REQUEST)


class LikeCount(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def list(self, request):
        obj = Likes.objects.values('post_id').annotate(count=Count('user_id'))
        return Response(obj)


class FollowersViewset(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            user_id = request.user
            if Followers.objects.filter(user_id=user_id,
                                        followers_id=data.get('followers_id')).exists():
                return Response({'msg': 'this user alredy follower '}, status=HTTP_429_TOO_MANY_REQUESTS)

            Followers.objects.create(
                user_id=Profile.objects.get(username=user_id),
                followers_id=Profile_Page.objects.get(uuid=data.get('followers_id')),
            )

            return Response({'msg': 'followed...!'}, status=HTTP_201_CREATED)


        except Exception as e:
            print(e)
            return Response({'msg': 'something went wrong'}, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        try:
            data = request.data
            unfollow = Followers.objects.filter(followers_id=data.get('followers_id'))
            if not unfollow.exists():
                return Response({'alredy unfollwed...'}, status=HTTP_400_BAD_REQUEST)
            unfollow[0].delete()
            return Response({'msg': 'unfollowed...'}, status=HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'msg': 'something went wrong '}, status=HTTP_400_BAD_REQUEST)


class FollowersCount(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        obj = Followers.objects.filter(user_id= request.user).values('user_id').annotate(followers=Count('user_id'))
        return Response(obj)

class Followers_ids(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self,request):
        try:
            object = Followers.objects.filter(user_id = request.user).values_list('followers_id')
            return Response(object)

        except Exception as e:
            print(e)

class Following_ids(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self,request):
        try:
            object = Following.objects.filter(user_id = request.user).values_list('following_id')
            return Response(object,status=HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({'msg':'400 bad request'},status=HTTP_400_BAD_REQUEST)

 
class FollowingViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self,request,*args,**kwargs):
        try:
            obj = Following.objects.filter(user_id=request.user).values('user_id').annotate(
                following=Count('following_id'))
            return Response(obj,status=HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'msg':'400 '},status=HTTP_400_BAD_REQUEST)


    def create(self,request,*args,**kwargs):
        try:
            Following.objects.create(user_id = request.user,
                                     following_id = Profile_Page.objects.get(uuid = request.data.get('following_id')))
            return Response({'msg':'following ...!'},status=HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({'msg':'400  bad request'},status=HTTP_400_BAD_REQUEST)

class Profiles_list(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Profile_Page.objects.all()
    serializer_class = Profile_Page_Serializer
    filter_backends = [SearchFilter]
    search_fields = ['$name']


    def get_queryset(self):
        queryset = Profile_Page.objects.all()
        username = self.request.query_params.get('name')
        if username is not None:
            queryset = queryset.filter(Profile_Page__name=username)
        return queryset

class CommentsViewset(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            user_id = request.user

            Comments.objects.create(user_id=Profile.objects.get(username = user_id),
                                    post_id = Posts.objects.get(uuid = data.get('post_id')),
                                    message = data.get('message'))
            return Response({'msg':'comment is posted '},status=HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({'msg':'something went wrong'},status=HTTP_400_BAD_REQUEST)


    def list(self,request,*args,**kwargs):
        try:
            object = Comments.objects.all()
            serializer = CommentSerializer(object,many=True).data
            return Response(serializer)

        except Exception as e:
            print(e)
            return Response(status=HTTP_400_BAD_REQUEST)




class StoriesView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def create(self,request,*args,**kwargs):
        try:
            data = request.data
            user_id  = request.user
            Stories.objects.create(user_id = Profile.objects.get(username = user_id),
                                   Profile_id = Profile_Page.objects.get(uuid = request.data.get('Profile_id')),
                                   file = data.get('file'),
                                   expiridate = datetime.datetime.now() + datetime.timedelta(hours=24),
                                   ),

            return Response({'data':{'msg':'story uploded...'}},status=HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({'error':e},status=HTTP_400_BAD_REQUEST)

