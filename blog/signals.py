from django.db.models import signals
from .models import Post


def increment_comment_count(sender, instance, created, raw, **kwargs):
    if created:
        instance.post.comment_count += 1
        instance.post.save()


def decrement_comment_count(sender, instance, **kwargs):
    instance.post.comment_count -= 1
    instance.post.save()


signals.post_save.connect(increment_comment_count, sender=Post)
signals.post_delete.connect(decrement_comment_count, sender=Post)
