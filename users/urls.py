from django.urls import path
from users import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('profiles/', views.profiles, name="profiles"),
    path('profile/<str:pk>/', views.profile, name="profile"),
    path('login/', views.userLogin, name="login"),
    path('logout/', views.userLogout, name="logout"),
    path('logout-page/', views.userLogoutPage, name="logout-page"),
    path('register/', views.userRegister, name="register"),
    path('edit-profile/', views.editProfile, name="edit-profile"),
    path('messages-view/', views.messagesView, name="messages-view"),
    path('message-view/<str:pk>/', views.messageView, name="message-view"),
    path('create-message/<str:pk>/', views.createMessage, name="create-message"),
    path('change-password/', views.changePassword, name="change-password"),
]
