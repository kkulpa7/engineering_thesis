from django.urls import path
from blog import views

urlpatterns = [
    path('posts/', views.posts, name="posts"),
    path('post/<str:pk>/', views.post, name="post"),
    path('create-post/', views.createPost, name="create-post"),
    path('update-post/<str:pk>', views.updatePost, name="update-post"),
    path('delete-post/<str:pk>', views.deletePost, name="delete-post"),
]
