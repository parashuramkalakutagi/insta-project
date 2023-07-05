
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from accounts.views import *

accounts = DefaultRouter()

accounts.register('profile',Profile_Register,basename='profile')
accounts.register('Login',LoginViewset,basename='Login')
accounts.register('LogOut',LogOutViewset,basename='LogOut')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include(accounts.urls)),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
