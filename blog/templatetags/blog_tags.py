from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe

import markdown

from ..models import Post

register = template.Library()


@register.simple_tag
def total_posts():
    """
    Retrieve the total post published on the blog
    """
    return Post.published.count()


@register.inclusion_tag('tags/latest_posts.html')
def show_latest_posts(count=3):
    """
    Inclusion tag to display latest posts in the sidebar
    """
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


@register.simple_tag
def get_most_commented_posts(count=5):
    # aggregrate the total number of comments for each post
    # and order the queryset by the computed field in desc order
    return Post.published.annotate(
        total_comments=Count('comments')
    ).order_by('-total_comments')[:count]


@register.filter(name='markdown')
def markdown_format(text):
    """ Filter for MD blog posts """
    return mark_safe(markdown.markdown(text))
