from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm, PostForm, ProfileForm
from .models import Category, Comment, Post, User
from .services import comment_counter, common_filter, get_paginator


def index(request):
    page_obj = get_paginator(common_filter(comment_counter(Post.objects)),
                             request.GET.get('page'))
    return render(request, 'blog/index.html', {'page_obj': page_obj})


def post_detail(request, post_id):
    post = get_object_or_404(Post.objects, pk=post_id)
    form = CommentForm()
    if post.author != request.user:
        post = get_object_or_404(common_filter(Post.objects), pk=post_id)
    return render(request, 'blog/detail.html',
                  {'post': post,
                   'form': form,
                   'comments': post.comments.all()})


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    page_obj = get_paginator(common_filter(comment_counter(category.posts)),
                             request.GET.get('page'))
    return render(request, 'blog/category.html', {'category': category,
                                                  'page_obj': page_obj})


def profile(request, username):
    profile = get_object_or_404(User, username=username)
    page_obj = comment_counter(profile.posts)
    if request.user != profile:
        page_obj = common_filter(page_obj)
    page_obj = get_paginator(page_obj, request.GET.get('page'))
    return render(request, 'blog/profile.html',
                  {'profile': profile, 'page_obj': page_obj})


@login_required
def edit_profile(request):
    profile = get_object_or_404(User, username=request.user.username)
    form = ProfileForm(request.POST or None, instance=profile)
    if form.is_valid():
        form.save()
        return redirect('blog:profile', username=request.user.username)
    return render(request, 'blog/user.html', {'form': form})


@login_required
def create_post(request):
    form = PostForm(request.POST or None, files=request.FILES or None,)
    if not form.is_valid():
        return render(request, 'blog/create.html', {'form': form})
    post = form.save(commit=False)
    post.author = request.user
    post.save()
    return redirect('blog:profile', request.user.username)


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.author:
        return redirect('blog:post_detail', post_id=post_id)
    form = PostForm(request.POST, instance=post, files=request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', post_id=post_id)
    form = PostForm(instance=post)
    return render(request, 'blog/create.html', {'form': form})


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('blog:post_detail', post_id)


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        return redirect('blog:post_detail', post_id)
    form = PostForm(request.POST or None, instance=post)
    if request.method == 'POST':
        post.delete()
        return redirect('blog:index')
    return render(request, 'blog/create.html', {'form': form})


@login_required
def edit_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id, post__id=post_id)
    if comment.author != request.user:
        return redirect('blog:post_detail', post_id=post_id)
    form = CommentForm(request.POST or None, instance=comment)
    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', post_id=post_id)
    return render(request, 'blog/comment.html',
                  {'form': form, 'comment': comment})


@login_required
def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id,
                                post_id=post_id)

    if comment.author == request.user and request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail', post_id=post_id)
    return render(request, 'blog/comment.html', {'comment': comment})
