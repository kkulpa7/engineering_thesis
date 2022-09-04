from django.urls import path, re_path
from blog import views

urlpatterns = [
    path('posts/', views.posts, name="posts"),
    path('post/<str:pk>/', views.post, name="post"),
    path('create-post/', views.createPost, name="create-post"),
    path('update-post/<str:pk>', views.updatePost, name="update-post"),
    path('delete-post/<str:pk>', views.deletePost, name="delete-post"),
    path('user-posts/', views.userPosts, name="user-posts"),
    # path('tag/<slug:slug>/', views.tagged, name="tagged"),
    re_path(r'^tag/(?P<slug>[-\w]*)/$', views.tagged, name="tagged"),
]
