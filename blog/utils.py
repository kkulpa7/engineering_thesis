from django.db.models import Q
from django.shortcuts import get_object_or_404
from taggit.models import Tag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post


def searchPosts(request, user=False):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    if user:
        profile = request.user.profile
        posts = Post.objects.distinct().filter(
            Q(author=profile) &
            (Q(title__icontains=search_query) |
            Q(text__icontains=search_query))
        )
    else:
        posts = Post.objects.distinct().filter(
            Q(title__icontains=search_query) |
            Q(text__icontains=search_query)
            )

    return posts, search_query


def paginatePosts(request, posts, results):
    page = request.GET.get('page')
    paginator = Paginator(posts, results)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        posts = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        posts = paginator.page(page)

    leftIndex = (int(page) - 3)

    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page) + 4)

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_rage = range(leftIndex, rightIndex)
    return custom_rage, posts
