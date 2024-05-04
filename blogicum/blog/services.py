from django.core.paginator import Paginator
from django.db.models import Count
from django.utils.timezone import now

from .constants import POSTS_PER_PAGE


def common_filter(model_objects):
    return model_objects.filter(
        pub_date__lt=(now()), is_published=True, category__is_published=True
    )


def get_paginator(post_list, page):
    paginator = Paginator(post_list, POSTS_PER_PAGE)
    page_obj = paginator.get_page(page)
    return page_obj


def comment_counter(posts):
    return posts.select_related(
        'category', 'location', 'author'
    ).annotate(comment_count=Count(
        'comments'
    )).order_by('-pub_date')
