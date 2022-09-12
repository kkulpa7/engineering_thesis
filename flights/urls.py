from django.urls import path
from flights import views

urlpatterns = [
    path('flights/', views.flightsView, name='flights'),
    path('flight-results/<str:pk>/', views.flightResults, name="flight-results"),
]
