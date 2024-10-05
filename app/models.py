from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=News.Status.PUBLISHED)


class Contact(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(max_length=150)
    message = models.TextField()

    def __str__(self):
        return self.email


class Category(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class News(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)
    body = models.TextField()
    image = models.ImageField(upload_to='news/images', default='news/default.jpeg')
    category = models.ForeignKey('app.Category',
                                 on_delete=models.CASCADE,
                                 related_name='news')
    publish_time = models.DateTimeField(default=timezone.now)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT)

    objects = models.Manager()  # default manager
    published = PublishedManager()  # custom manager

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news_detail_page', args=[self.slug])

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class Comments(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='comments',
                             related_query_name='comment')
    new = models.ForeignKey(News,
                            on_delete=models.CASCADE,
                            related_name='comments',
                            related_query_name='comment')

    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.user}"
