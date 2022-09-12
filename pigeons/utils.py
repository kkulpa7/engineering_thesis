from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Pigeon


def searchPigeons(request, user=False):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    if user:
        profile = request.user.profile
        pigeons = Pigeon.objects.distinct().filter(
            Q(owner=profile) &
            Q(number__icontains=search_query)
        )
    else:
        pigeons = Pigeon.objects.distinct().filter(
            Q(number__icontains=search_query)
            )

    return pigeons, search_query


def paginatePigeons(request, pigeons, results):
    page = request.GET.get('page')
    paginator = Paginator(pigeons, results)

    try:
        pigeons = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        pigeons = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        pigeons = paginator.page(page)

    leftIndex = (int(page) - 3)

    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page) + 4)

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_rage = range(leftIndex, rightIndex)
    return custom_rage, pigeons


def pigeonParents(pigeons):
    return_list = []
    for pigeon in pigeons:
        if pigeon:
            if pigeon.mother:
                return_list.extend([Pigeon.objects.get(id=pigeon.mother.id)])
            else:
                return_list.extend([None])
            if pigeon.father:
                return_list.extend([Pigeon.objects.get(id=pigeon.father.id)])
            else:
                return_list.extend([None])
        else:
            return_list.extend([None, None])

    return return_list
