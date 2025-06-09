from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=50)
    views = models.IntegerField(default=0, blank=True)
    slug = models.SlugField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Service(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    icon = models.FileField(upload_to='services/icons/', null=True, blank=True)  # Changed from ImageField
    slug = models.SlugField(max_length=200)
    views = models.IntegerField(default=0, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    views = models.IntegerField(default=0, blank=True)
    slug = models.SlugField(max_length=200)
    image_url = models.FileField(upload_to='projects/images/')  # Changed from ImageField
    project_url = models.CharField(max_length=255, blank=True, null=True)
    keywords = models.TextField()
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class ProjectWorker(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Article(models.Model):
    title = models.CharField(max_length=100)
    post = models.TextField()
    likes = models.IntegerField(default=0, blank=True)
    dislikes = models.IntegerField(default=0, blank=True)
    slug = models.SlugField(max_length=200)
    image_url = models.FileField(upload_to='articles/images/')  # Changed from ImageField
    views = models.IntegerField(default=0, blank=True)
    keywords = models.TextField()
    STATUS_CHOICES = (
        ('P', 'Published'),
        ('D', 'Draft'),
        ('S', 'Scheduled')
    )
    status = models.CharField(default="Published", max_length=1001)
    schedule_date = models.DateTimeField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    message = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, blank=False, null=False)
    likes = models.IntegerField(default=0, blank=True)
    dislikes = models.IntegerField(default=0, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message

class Feedback(models.Model):
    message = models.TextField()
    name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    phone_number = models.IntegerField(blank=True, null=True)
    TYPE_CHOICES = (
        ('G', 'General'),
        ('Q', 'Quote'),
    )
    status = models.IntegerField(default=0)
    type = models.CharField(blank=True, null=True, choices=TYPE_CHOICES, max_length=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email

class Seo(models.Model):
    title = models.CharField(max_length=100)
    keywords = models.TextField()
    occasion = models.CharField(max_length=50)
    site_views = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
