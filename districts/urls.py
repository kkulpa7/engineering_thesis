from django.urls import path
from districts import views

urlpatterns = [
    path('districts/', views.districtsView, name='districts'),
]
