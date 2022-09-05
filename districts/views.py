from django.shortcuts import render
from .models import District, Branch

# Create your views here.
def districtsView(request):
    districts = District.objects.all()
    branches = Branch.objects.all()

    context = {
        'districts': districts,
        'branches': branches,
    }
    return render(request, 'districts/districts-view.html', context)
