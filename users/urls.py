from django.urls import path
from users import views

urlpatterns = [
    path('profiles/', views.profiles, name="profiles"),
    path('profile/<str:pk>', views.profile, name="profile"),
    path('login/', views.userLogin, name="login"),
    path('logout/', views.userLogout, name="logout"),
    path('logout-page/', views.userLogoutPage, name="logout-page"),
    path('register/', views.userRegister, name="register"),
    path('edit-profile/', views.editProfile, name="edit-profile"),
]
