from django.urls import path
from . import views
from .feeds import LatestPostsFeed

app_name = 'blog'

urlpatterns = [
    path('create/', views.create, name='create'),
    path('update/<int:pk>/', views.update, name='update'),
    path('delete/<int:pk>/', views.delete, name='delete'),
    path('tags/<slug:tag>/', views.home, name='posts_by_tag'),
    path('<slug:slug>/', views.detail, name='detail'),
    path('', views.home, name='post_list'),
    # path('<int:year>/<int:month>/<int:day>/<slug:slug>/',
    #      views.detail, name='detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('feed/', LatestPostsFeed(), name='post_feed'),
    # path('search/', post_search, name='post_search'),
]
