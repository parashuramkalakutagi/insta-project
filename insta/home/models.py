# from django.db import models
# import uuid
# from accounts.models import Profile
#
# class BaseModel(models.Model):
#     uuid = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now = True)
#
#     class Meta:
#         abstract  = True
#
# class Profile_Page(BaseModel):
#     user = models.ForeignKey(Profile,on_delete=models.CASCADE)
#     name = models.CharField(max_length=100)
#     bio = models.CharField(max_length=250,null=True,blank=True)
#     slug = models.URLField(max_length=200,null=True,blank=True)



