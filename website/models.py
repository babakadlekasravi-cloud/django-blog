from django.db import models

# Create your models here.
class Ticket(models.Model):
    name=models.CharField(max_length=200)
    subject=models.CharField(max_length=200,blank=True)
    email=models.EmailField()
    message=models.TextField(blank=True)
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering=['-created_date']