from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Pigeon
from .forms import PigeonForm
from .utils import searchPigeons, paginatePigeons

from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

# Create your views here.
def pigeons(request):
    pigeons = Pigeon.objects.all()

    context = {'pigeons': pigeons}
    return render(request, 'pigeons/pigeons.html', context)


@login_required(login_url="login")
def createPigeon(request):
    profile = request.user.profile
    form = PigeonForm()

    if request.method == 'POST':
        form = PigeonForm(request.POST, request.FILES)
        if form.is_valid():
            pigeon = form.save(commit=False)
            pigeon.owner = profile
            pigeon.save()

            messages.success(request, 'Udało się dodać gołębia!')

            return redirect('user-pigeons')

    context = {'form': form, 'type': 0}
    return render(request, 'pigeons/pigeon-form.html', context)

@login_required(login_url="login")
def updatePigeon(request, pk):
    pigeon = Pigeon.objects.get(id=pk)
    form = PigeonForm(instance=pigeon)

    if request.method == 'POST':
        form = PigeonForm(request.POST, request.FILES, instance=pigeon)
        if form.is_valid():
            form.save()
            messages.success(request, 'Udało się edytować gołębia!')
            return redirect('user-pigeons')

    context = {'form': form, 'type': 1}
    return render(request, 'pigeons/pigeon-form.html', context)


@login_required(login_url="login")
def userPigeons(request):
    pigeons, search_query = searchPigeons(request, user=True)

    male = pigeons.filter(gender='M').count()
    female = pigeons.filter(gender='F').count()
    unknown = pigeons.filter(gender=None).count()


    custom_rage, pigeons = paginatePigeons(request, pigeons, 10)

    context = {
        'pigeons': pigeons,
        'search_query': search_query,
        'custom_rage': custom_rage,
        'male': male,
        'female': female,
        'unknown': unknown
    }
    return render(request, 'pigeons/user-pigeons.html', context)


def pigeonLineage(request, pk):
    pigeon = Pigeon.objects.get(id=pk)
    context = {'pigeon': pigeon}
    return render(request, 'pigeons/pigeon-lineage.html', context)


@login_required(login_url="login")
def deletePigeon(request, pk):
    pigeon = Pigeon.objects.get(id=pk)

    if request.method == 'POST':
        pigeon.delete()
        return redirect('user-pigeons')

    context = {'pigeon': pigeon}
    return render(request, 'pigeons/delete-pigeon.html', context)

def pigeon(request, pk):
    pigeon = Pigeon.objects.get(id=pk)

    context = {'pigeon': pigeon}
    return render(request, 'pigeons/pigeon.html', context)


def genertePdf(request):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    textob = c.beginText()
    textob.setTextOrigin(inch,inch)
    textob.setFont("Helvetica", 14)

    lines = [
        "This is line 1",
        "This is line 2",
    ]

    for line in lines:
        textob.textLine(line)

    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename='cos.pdf')
