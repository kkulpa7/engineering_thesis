from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post, Comment
from .forms import PostForm, CommentForm
from .utils import searchPosts, paginatePosts

from taggit.models import Tag


# Create your views here.
def tagged(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(tags=tag)
    common_tags = Post.tags.most_common()[:4]
    context = {
        'tag': tag,
        'posts': posts,
        'common_tags': common_tags,
    }
    return render(request, 'blog/posts.html', context)


def posts(request):
    posts, search_query = searchPosts(request)
    custom_rage, posts = paginatePosts(request, posts, 6)
    common_tags = Post.tags.most_common()[:4]

    context = {
        'posts': posts,
        'search_query': search_query,
        'custom_rage': custom_rage,
        'common_tags': common_tags,
    }
    return render(request, 'blog/posts.html', context)


def post(request, pk):
    post = Post.objects.get(id=pk)
    comments = post.comments.all()
    form = CommentForm()

    if request.method == "POST":
        form = CommentForm(request.POST)
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user.profile
        comment.save()

        post.getVoteCount

        messages.success(request, 'Udało się dodać komentarz.')

        return redirect('post', pk=post.id)

    context = {
        'post': post,
        'comments': comments,
        'form': form
    }
    return render(request, 'blog/post.html', context)


@login_required(login_url="login")
def userPosts(request):
    posts, search_query = searchPosts(request, user=True)
    custom_rage, posts = paginatePosts(request, posts, 3)

    context = {
        'posts': posts,
        'search_query': search_query,
        'custom_rage': custom_rage
    }
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

            form.save_m2m()

            messages.success(request, 'Udało się dodać post!')

            return redirect('posts')

    context = {
        'form': form,
        'type': 0,
    }
    return render(request, 'blog/post_form.html', context)


@login_required(login_url="login")
def updatePost(request, pk):
    profile = request.user.profile
    post = profile.posts.get(id=pk)
    form = PostForm(instance=post)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Udało się edytować post ' + post.title + '!')
            return redirect('posts')

    context = {
        'form': form,
        'type': 1,
    }
    return render(request, 'blog/post_form.html', context)


@login_required(login_url="login")
def deletePost(request, pk):
    profile = request.user.profile
    post = profile.posts.get(id=pk)

    if request.method == 'POST':
        post.delete()
        return redirect('posts')

    context = {'post': post}
    return render(request, 'blog/delete_post.html', context)
