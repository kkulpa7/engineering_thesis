from django.urls import path
from pigeons import views

urlpatterns = [
    path('pigeons/', views.pigeons, name="pigeons"),
    path('user-pigeons/', views.userPigeons, name="user-pigeons"),
    path('create-pigeon/', views.createPigeon, name="create-pigeon"),
    path('update-pigeon/<str:pk>/', views.updatePigeon, name="update-pigeon"),
    path('pigeon-lineage/<str:pk>/', views.pigeonLineage, name="pigeon-lineage"),
    path('delete-pigeon/<str:pk>/', views.deletePigeon, name="delete-pigeon"),
    path('pigeon/<str:pk>/', views.pigeon, name="pigeon"),
    path('generate-pdf/', views.genertePdf, name="generate-pdf"),
]
