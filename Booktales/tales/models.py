from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Tales(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default="Untitled")
    text = models.TextField(max_length=5000)
    photo = models.ImageField(upload_to='tales/', blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    bookmarked_by = models.ManyToManyField(User, related_name="bookmarked", blank=True) 

    def __str__(self):
        return f'{self.user.username} - {self.title}'
