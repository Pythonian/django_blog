import datetime
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from taggit.managers import TaggableManager
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill

from django.core.validators import MinLengthValidator

content_validator = MinLengthValidator(
    limit_value=300, message="Content should be at least 300 characters long!")


class Tag(models.Model):
    title = models.CharField(max_length=20)
    slug = models.SlugField(max_length=20)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:tag', args=[str(self.slug)])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Category(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class PostQuerySet(models.query.QuerySet):
    def public(self):
        return self.filter(draft=False)

    def published(self):
        return self.filter(date__gte=datetime.datetime.now())


class PostManager(models.Manager):
    """ Post.objects.public().published().order_by('date') """
    # def get_queryset(*args, **kwargs):
    #     return super().get_queryset(*args, **kwargs).filter(
    #         draft=False)

    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)

    def public(self):
        return self.get_queryset().public()

    def published(self):
        return self.get_queryset().published()


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()\
                      .filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,
                            unique_for_date='publish')
    body = models.TextField(validators=[content_validator])
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name='blog_posts')
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES, default='draft')
    # models.PROTECT prevents deletion of category if a Post instance exists
    category = models.ForeignKey(Category, null=True, on_delete=models.PROTECT)
    tags = TaggableManager()
    # tags = models.ManyToManyField(Tag, blank=True)
    image = models.ImageField(upload_to='images')
    image_thumbnail = ImageSpecField(source='image',
                                     processors=[ResizeToFill(700, 150)],
                                     format='JPEG', options={'quality': 60})
    comment_count = models.PositiveIntegerField(default=0)

    objects = models.Manager()
    published = PublishedManager()
    # objects = PostManager

    class Meta:
        ordering = ['-publish']
        get_latest_by = 'publish'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_previous_post(self):
        return self.get_previous_by_publish()

    def get_next_post(self):
        return self.get_next_by_publish()

    def get_absolute_url(self):
        return reverse('blog:detail', args=[str(self.slug)])

    # def get_absolute_url(self):
    #     return reverse('blog:detail',
    #                    args=[self.publish.year,
    #                          self.publish.month,
    #                          self.publish.day,
    #                          self.slug])


class Comment(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return f"Comment by {self.name} on {self.post}"
