"""nikah URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include 
from django.conf import settings 
from django.conf.urls.static import static

from marriage import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index),
    path('admin/', admin.site.urls),
    path('index/', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    
    path('cabinet/', views.cabinet, name='cabinet'),
    #path('person/edit/<int:id>/', views.person_edit, name='person_edit'),
    path('person/edit/', views.person_edit, name='person_edit'),
    path('person/list/', views.person_list, name='person_list'),
    path('person/read/<int:id>/', views.person_read, name='person_read'),
    
    path('message/index/', views.message_index, name='message_index'),

    path('friend/index/', views.friend_index, name='friend_index'),
    path('friend/list/', views.friend_list, name='friend_list'),
    path('friend/create/<int:id>/', views.friend_create, name='friend_create'),
    path('friend/confirm/<int:id>/', views.friend_confirm, name='friend_confirm'),
    #path('friend/edit/<int:id>/', views.friend_edit, name='friend_edit'),
    #path('friend/delete/<int:id>/', views.friend_delete, name='friend_delete'),
    #path('friend/read/<int:id>/', views.friend_read, name='friend_read'),
    
    #path('photo/index/', views.photo_index, name='photo_index'),
    #path('photo/list/', views.photo_list, name='photo_list'),
    #path('photo/create/', views.photo_create, name='photo_create'),
    #path('photo/edit/<int:id>/', views.photo_edit, name='photo_edit'),
    #path('photo/delete/<int:id>/', views.photo_delete, name='photo_delete'),
    #path('photo/read/<int:id>/', views.photo_read, name='photo_read'),

    path('status/index/', views.status_index, name='status_index'),
    path('status/list/', views.status_list, name='status_list'),
    path('status/create/', views.status_create, name='status_create'),
    path('status/edit/<int:id>/', views.status_edit, name='status_edit'),
    path('status/delete/<int:id>/', views.status_delete, name='status_delete'),
    path('status/read/<int:id>/', views.status_read, name='status_read'),

    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('settings/account/', views.UserUpdateView.as_view(), name='my_account'),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('password-change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
