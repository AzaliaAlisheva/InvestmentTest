from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index),
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
    path('polls/', include('polls.urls')),
    path('posts/', include('posts.urls')),
]