from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings  #use settings.AUTH_USER_MODEL

# Create your models here.

#Category model
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    def __str__(self):
        return self.name

#Post model
class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

#Comment model
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'comment by {self.author} on {self.post}'

#CustomUser model
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    class Meta:
        swappable = 'AUTH_USER_MODEL'  # Ensures Django replaces default User

