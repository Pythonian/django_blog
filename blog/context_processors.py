from .models import Post


def latest_posts(request):
    posts = Post.objects.filter().order_by('-created')[:3]
    return {'latest_posts': posts}
