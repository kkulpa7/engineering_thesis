from django.shortcuts import render
from .models import Flight, Result

# Create your views here.
def flightsView(request):
    flights = Flight.objects.all()

    context = {
        'flights': flights,
    }
    return render(request, 'flights/flights.html', context)


def flightResults(request, pk):
    flight = Flight.objects.get(id=pk)
    results = Result.objects.filter(flight=flight)

    context = {
        'flight': flight,
        'results': results,
    }

    return render(request, 'flights/flight-results.html', context)
