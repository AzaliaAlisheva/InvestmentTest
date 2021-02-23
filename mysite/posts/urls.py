from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'posts'
urlpatterns = [
    path('', views.index, name='blog'),
    path('<int:pk>/', views.PostDetailView.as_view(), name='post details'),
    path('<int:pk>/update/', views.PostUpdateView.as_view(), name='post update'),
    path('new_post/', views.new_post, name='new post'),
    path('my_posts/', views.my_posts, name='my posts'),
    path('successful_new_request/', views.successful_new_request, name='successful new post'),
    path('personal_account/', views.personal_account, name='personal account'),
]
