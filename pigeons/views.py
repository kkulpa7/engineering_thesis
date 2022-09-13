from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Pigeon
from flights.models import Result
from .forms import PigeonForm
from .utils import searchPigeons, paginatePigeons, pigeonParents

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
            messages.success(request, 'Udało się edytować gołębia o numerze ' + "'" + pigeon.number + "'!")
            return redirect('pigeon', pk=pigeon.id)

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

    parents = pigeonParents([pigeon])
    grandparents = pigeonParents(pigeonParents([pigeon]))
    greatgrandparents = pigeonParents(pigeonParents(pigeonParents([pigeon])))
    greatgreatgrandparents = pigeonParents(pigeonParents(pigeonParents(pigeonParents([pigeon]))))

    generation_list = []
    generation_list.extend(parents)
    generation_list.extend(grandparents)
    generation_list.extend(greatgrandparents)
    generation_list.extend(greatgreatgrandparents)

    generation_list_colors = []

    color = 1

    for i in list(set(generation_list)):
        if generation_list.count(i) == 1 or i == None:
            generation_list_colors.extend([[i, 0]])
        else:
            generation_list_colors.extend([[i, color]])
            color += 1

    print(generation_list_colors)

    context = {
        'pigeon': pigeon,
        'parents': parents,
        'grandparents': grandparents,
        'greatgrandparents': greatgrandparents,
        'greatgreatgrandparents': greatgreatgrandparents,
        'generation_list_colors': generation_list_colors
    }

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

    children = Pigeon.objects.distinct().filter(
        Q(mother=pigeon) |
        Q(father=pigeon)
    )
    results = Result.objects.distinct().filter(
        Q(pigeon=pigeon)
    )

    context = {
        'pigeon': pigeon,
        'children': children,
        'results': results,
    }
    return render(request, 'pigeons/pigeon.html', context)


def genertePdf(request, pk):
    pigeon = Pigeon.objects.get(id=pk)


    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    textob = c.beginText()
    textob.setTextOrigin(inch,inch)
    textob.setFont("Helvetica", 14)

    parents = pigeonParents([pigeon])
    grandparents = pigeonParents(pigeonParents([pigeon]))
    greatgrandparents = pigeonParents(pigeonParents(pigeonParents([pigeon])))
    greatgreatgrandparents = pigeonParents(pigeonParents(pigeonParents(pigeonParents([pigeon]))))

    textob.textLine("Wlasciciel golebia")
    textob.textLine(pigeon.owner.first_name + " " + pigeon.owner.last_name)

    textob.textLine(" ")
    textob.textLine("Rodowod golebia o numerze " + pigeon.number)

    textob.textLine(" ")
    textob.textLine("Rodzice golebia: ")

    for parent in parents:
        if parent:
            textob.textLine(parent.number)
        else:
            textob.textLine("#")

    textob.textLine(" ")
    textob.textLine("Dziadkowie golebia: ")

    for parent in grandparents:
        if parent:
            textob.textLine(parent.number)
        else:
            textob.textLine("#")

    textob.textLine(" ")
    textob.textLine("Pradziadkowie golebia: ")

    for parent in greatgrandparents:
        if parent:
            textob.textLine(parent.number)
        else:
            textob.textLine("#")

    textob.textLine(" ")
    textob.textLine("Prapradziadkowie golebia: ")

    for parent in greatgreatgrandparents:
        if parent:
            textob.textLine(parent.number)
        else:
            textob.textLine("#")

    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename='rodowod_' + pigeon.number + '.pdf')
