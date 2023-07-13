
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from accounts.views import *
from home.views import *

accounts = DefaultRouter()

accounts.register('profile',Profile_Register,basename='profile')
accounts.register('Login',LoginViewset,basename='Login')
accounts.register('LogOut',LogOutViewset,basename='LogOut')
accounts.register('ForgotPassword',ForgotPasswordViewset,basename='ForgotPassword')
accounts.register('verifyOtpView',verifyOtpView,basename='verifyOtpView')
accounts.register('NewPassword',NewPassword,basename='NewPassword')

home = DefaultRouter()

home.register('ProfileView',ProfileView,basename='ProfileView')
home.register('post',PostView,basename='PostView')
home.register('POST_LIST',POST_LIST,basename='POST_LIST')
home.register('VideoPostViewset',VideoPostViewset,basename='VideoPostViewset')
home.register('HighlightesView',HighlightesView,basename='HighlightesView')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('acc/',include(accounts.urls)),
    path('home/',include(home.urls)),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
