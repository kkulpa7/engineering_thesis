from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post, Comment, Tag
from .forms import PostForm
from .utils import searchPosts, paginatePosts


# Create your views here.
def posts(request):
    posts, search_query = searchPosts(request)
    custom_rage, posts = paginatePosts(request, posts, 6)

    context = {'posts': posts, 'search_query': search_query, 'custom_rage': custom_rage}
    return render(request, 'blog/posts.html', context)


def post(request, pk):
    post = Post.objects.get(id=pk)
    context = {'post': post}
    return render(request, 'blog/post.html', context)


@login_required(login_url="login")
def userPosts(request):
    posts, search_query = searchPosts(request, user=True)
    custom_rage, posts = paginatePosts(request, posts, 3)

    context = {'posts': posts, 'search_query': search_query, 'custom_rage': custom_rage}
    return render(request, 'blog/user-posts.html', context)


@login_required(login_url="login")
def createPost(request):
    profile = request.user.profile
    form = PostForm()

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = profile
            post.save()

            messages.success(request, 'Udało się dodać post!')

            return redirect('posts')

    context = {'form': form, 'type': 0}
    return render(request, 'blog/post_form.html', context)


@login_required(login_url="login")
def updatePost(request, pk):
    post = Post.objects.get(id=pk)
    form = PostForm(instance=post)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Udało się edytować post!')
            return redirect('posts')

    context = {'form': form, 'type': 1}
    return render(request, 'blog/post_form.html', context)


@login_required(login_url="login")
def deletePost(request, pk):
    post = Post.objects.get(id=pk)

    if request.method == 'POST':
        post.delete()
        return redirect('posts')

    context = {'post': post}
    return render(request, 'blog/delete_post.html', context)
