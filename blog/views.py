from django.contrib.auth.decorators import permission_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator, InvalidPage
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (
    CreateView, DetailView, DeleteView, ListView, UpdateView)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from taggit.models import Tag
from django.db.models import Count
from .models import Post
from .forms import PostForm, PostDeleteForm, CommentForm, EmailPostForm
from django.core.mail import send_mail


def mk_paginator(request, items, num_items):
    '''Create and return a paginator.'''
    paginator = Paginator(items, num_items)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        items = paginator.page(page)
    except (InvalidPage, EmptyPage):
        items = paginator.page(paginator.num_pages)
    return items


def home(request, tag=None):
    tag_obj = None
    if not tag:
        posts = Post.objects.all()
    else:
        tag_obj = get_object_or_404(Tag, slug=tag)
        posts = Post.objects.filter(tags__in=[tag_obj])
        # posts = Post.objects.filter(tags__slug=tag_slug)

    paginator = Paginator(posts, 2)
    page = request.GET.get('page')
    try:
        # obtain the objects for the desired page
        posts = paginator.page(page)
    except PageNotAnInteger:
        # return first page
        posts = paginator.page(1)
    except EmptyPage:
        # return last page if page is out of range
        posts = paginator.page(paginator.num_pages)
    # posts = mk_paginator(request, posts, 10)

    template = 'home.html'
    context = {
        'section': 'home',
        'posts': posts,
        'tag': tag,
        'page': page
    }
    return render(request, template, context)


def detail(request, slug=None):
    post = get_object_or_404(Post, slug=slug)
    template = 'blog/detail.html'
    context = {'section': 'blog_detail', 'post': post}
    return render(request, template, context)


class PostListView(ListView):
    model = Post
    paginate_by = 3


class PostDetailView(DetailView):
    model = Post


# def post_detail(request, year, month, day, slug):
#     post = get_object_or_404(Post,
#                              slug=slug, status='published',
#                              publish__year=year,
#                              publish__month=month,
#                              publish__day=day)

#     comments = post.comments.filter(active=True)
#     new_comment = None
#     if request.method == 'POST':
#         comment_form = CommentForm(data=request.POST)
#         if comment_form.is_valid():
#             new_comment = comment_form.save(commit=False)
#             # assign the new comment to the current post
#             new_comment.post = post
#             new_comment.save()
#     else:
#         comment_form = CommentForm()

#     # List of similar posts
#     # Get the ids of the tags of the current post
#     post_tags_ids = post.tags.values_list('id', flat=True)
#     # get all posts that contains these tags, exclude current post
#     similar_posts = Post.published.filter(tags__in=post_tags_ids)\
#                                   .exclude(id=post.id)
#     # count the number of tags shared by each posts;
#     # order the result by the number of shared tags & recent posts first
#     similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
#                                  .order_by('-same_tags', '-publish')[:4]

#     template = 'blog/post/detail.html'
#     context = {
#         'post': post,
#         'comment_form': comment_form,
#         'comments': comments,
#         'new_comment': new_comment,
#         'similar_posts': similar_posts,
#     }

#     return render(request, template, context)


@permission_required('blog.add_post', raise_exception=True)
def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            # form.save_m2m()
            return redirect(post.get_absolute_url())
    else:
        form = PostForm()
    template = 'blog/form.html'
    context = {'form': form, 'section': 'blog_create'}
    return render(request, template, context)


@permission_required('blog.change_post', raise_exception=True)
def update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect(post.get_absolute_url())
    else:
        form = PostForm(instance=post)
    template = 'blog/form.html'
    context = {'form': form, 'section': 'update', 'form': form}
    return render(request, template, context)


@permission_required('blog.delete_post', raise_exception=True)
def delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostDeleteForm(request.POST, instance=post)
        if form.is_valid():
            post.delete()
            return redirect('home')
    else:
        form = PostDeleteForm(instance=post)
    template = 'blog/delete.html'
    context = {'form': form, 'section': 'delete', 'form': form}
    return render(request, template, context)


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'admin@blog.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()

    template = 'blog/post/share.html'
    context = {
        'form': form,
        'post': post,
        'sent': sent,
    }

    return render(request, template, context)


# class BlogCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
#     model = Blog
#     fields = ['title', 'content']
#     success_message = "Blog Created Successfully!"

#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         return super().form_valid(form)


# class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
#     model = Blog
#     fields = ['title', 'content']
#     success_message = "Blog Updated Successfully!"

#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         return super().form_valid(form)

#     def test_func(self):
#         """
#         This method puts the conditional pass for the
#         UserPassesTestMixin to only allow access to this view
#         if the currently logged-in user is the author of the Post
#         """
#         blog = self.get_object()
#         if self.request.user == blog.author:
#             return True
#         else:
#             return False


# class BlogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
#     model = Blog
#     success_message = "Blog Deleted Successfully!"
#     success_url = "/"

#     def test_func(self):
#         blog = self.get_object()
#         if self.request.user == blog.author:
#             return True
#         else:
#             return False

#     def delete(self, request, *args, **kwargs):
#         messages.success(self.request, self.success_message)
#         return super().delete(request, *args, **kwargs)
