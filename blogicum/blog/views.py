from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import now

from blog.models import Category, Comment, Post
from .constants import POSTS_PER_PAGE
from .forms import CommentForm, PostForm, ProfileForm


User = get_user_model()


def comment_counter(posts):
    return posts.annotate(comment_count=Count(
        'comment'
    )).order_by('-pub_date')


def get_paginator(post_list, page):
    paginator = Paginator(post_list, POSTS_PER_PAGE)
    page_obj = paginator.get_page(page)
    return page_obj


def index(request):
    page_obj = get_paginator(common_filter(comment_counter(Post.objects)),
                             request.GET.get('page'))
    return render(request, 'blog/index.html', {'page_obj': page_obj})


def post_detail(request, post_id):
    post = get_object_or_404(Post.objects, pk=post_id)
    form = CommentForm()
    comments = Comment.objects.select_related(
        'author'
    ).filter(post_id=post.id)
    if post.author == request.user:
        return render(request, 'blog/detail.html',
                      {'post': post, 'form': form, 'comments': comments})
    else:
        post = get_object_or_404(common_filter(Post.objects), pk=post_id)
        return render(request, 'blog/detail.html',
                      {'post': post, 'form': form, 'comments': comments})


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


def common_filter(model_objects):
    return model_objects.select_related(
        'category', 'location', 'author'
    ).filter(pub_date__lt=(now()), is_published=True,
             category__is_published=True)


def profile(request, username):
    profile = get_object_or_404(User, username=username)
    if request.user == profile:
        page_obj = get_paginator(
            comment_counter(Post.objects.filter(
                author__username=username
            )),
            request.GET.get('page')
        )
        return render(request, 'blog/profile.html',
                      {'profile': profile, 'page_obj': page_obj})
    else:
        page_obj = get_paginator(
            common_filter(comment_counter(Post.objects.filter(
                author__username=username
            ))),
            request.GET.get('page')
        )
        return render(request, 'blog/profile.html',
                      {'profile': profile, 'page_obj': page_obj})


def edit_profile(request):
    profile = get_object_or_404(User, username=request.user.username)
    form = ProfileForm(request.POST or None, instance=profile)
    if request.user == profile and form.is_valid():
        form.save()
        return redirect('blog:profile', username=request.user.username)
    return render(request, 'blog/user.html', {'form': form})


@login_required
def create_post(request):
    form = PostForm(request.POST or None, files=request.FILES or None,)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('blog:profile', request.user.username)
    return render(request, 'blog/create.html', {'form': form})


def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = PostForm(request.POST or None, instance=post)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid() and post.author == request.user:
            form.save()
            return redirect('blog:post_detail', post_id=post_id)
        elif post.author != request.user:
            return redirect('blog:post_detail', post_id=post_id)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/create.html', {'form': form})


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.POST:
        form = CommentForm(request.POST)
    else:
        form = CommentForm()
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
        return redirect('blog:post_detail', post_id)
    return redirect('blog:post_detail', post_id)


def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = PostForm(request.POST or None, instance=post)
    if post.author == request.user and request.method == 'POST':
        post.delete()
        return redirect('blog:index')
    return render(request, 'blog/create.html', {'form': form})


def edit_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id, post__id=post_id)
    form = CommentForm(request.POST or None, instance=comment)
    if comment.author != request.user:
        return redirect('blog:post_detail', post_id=post_id)
    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', post_id=post_id)
    return render(request, 'blog/comment.html',
                  {'form': form, 'comment': comment})


def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id,
                                post_id=post_id)

    if comment.author == request.user and request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail', post_id=post_id)
    return render(request, 'blog/comment.html', {'comment': comment})
