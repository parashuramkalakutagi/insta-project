from django.db import models
import uuid
from accounts.models import Profile

class BaseModel(models.Model):
    uuid = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        abstract  = True

class Profile_Page(BaseModel):
    user = models.OneToOneField(Profile,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    bio = models.CharField(max_length=250,null=True,blank=True)
    slug = models.URLField(max_length=200,null=True,blank=True)
    gender = models.CharField(max_length=20, choices=(("male", "Male"), ("Female", "Female")))
    profile_photo = models.ImageField(upload_to='Profile-images', null=True, blank=True)

    def __str__(self):
        return self.name


class Posts(BaseModel):
    user_id  = models.ForeignKey(Profile,on_delete=models.CASCADE)
    Profile_id = models.ForeignKey(Profile_Page,on_delete=models.CASCADE)
    post = models.ImageField(upload_to='posts')



class VideoPost(BaseModel):
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    Profile_id = models.ForeignKey(Profile_Page,on_delete=models.CASCADE)
    file = models.FileField(upload_to='POST_VIDEOS')

class hightlites(BaseModel):
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    Profile_id = models.ForeignKey(Profile_Page,on_delete=models.CASCADE)
    stories = models.FileField(upload_to='STORIES')

class Likes(models.Model):
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    profile_id = models.ForeignKey(Profile_Page, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Posts,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user_id} is liked this post >>  {self.post_id}'

class Followers(models.Model):
    user_id = models.ForeignKey(Profile,on_delete=models.CASCADE)
    followers_id = models.ForeignKey(Profile_Page,on_delete=models.CASCADE,related_name='followers_id')

    def __str__(self):
        return f'{self.user_id} is following {self.followers_id}'

class Comments(models.Model):
    user_id = models.ForeignKey(Profile,on_delete=models.CASCADE)
    post_id = models.ForeignKey(Posts,on_delete=models.CASCADE)
    message = models.CharField(max_length=150)





