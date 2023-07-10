from rest_framework import serializers
from .models import *
from accounts.models import Profile

class Profile_Page_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Profile_Page
        exclude = ['created_at','updated_at']

    def validate(self, data):
        user = data['user']
        object = Profile_Page.objects.filter(user=user)
        if object.exists():
            raise serializers.ValidationError('user alredy exists...')
        return data


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = ['Profile_id','post']


class VideoPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoPost
        fields = ['Profile_id','file']