"""first URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.static import serve
from first import settings
from main.views import *

urlpatterns = [
    path('admin/', admin.site.urls),

    path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT
    }),

    path('', indexHandler, name='home'),

    path('news/', It),

    path('video/', Video),
    path('search/', Search, name='Video'),
    path('video/<int:course_int>/', courseHandler),

    path('news/<int:shi_int>/', shiHandler),
    path('news/add-article/', add.as_view(), name='add'),

    path('video//<int:vid_int>/', vidHandler),
    path('video/add-course/', CourseAdd.as_view(), name='CourseAdd'),

    path('reg/', Register, name='Register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),

    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='password/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="password/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password/password_reset_complete.html'), name='password_reset_complete'),
    path("password_reset/", Reset, name="Reset"),

    path('Profile/', profile, name='profile'),
    path('Profile/edit/', edit, name='edit'),

    path('AddUser/', adduser, name='adduser'),
    path('Users/<int:user_int>', groups, name='groups'),
    path('Users//<int:user_int>', userHandler),
    path('Users/', users),
    path('Users/group/<int:user_int>', change)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
