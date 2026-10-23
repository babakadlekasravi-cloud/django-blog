from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Post(models.Model):
    title=models.CharField(max_length=200)
    content=models.TextField()
    status=models.BooleanField(default=False)
    author=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    created_date=models.DateTimeField(default=timezone.now)
    updated_date=models.DateTimeField(auto_now=True,blank=True,null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering=['-created_date']

class Comment(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    subject=models.TextField()
    email=models.EmailField()
    approved=models.BooleanField()
    created_date=models.DateTimeField(auto_now_add=True)
    update_date=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
