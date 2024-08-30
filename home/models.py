from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms



# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=122)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=12)
    desc = models.TextField()
    date = models.DateField()
    
    def __str__(self):
        return self.name
    
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='books/')
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    name = models.CharField(max_length=100,)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    purchased_at = models.DateTimeField(auto_now_add=True)
    purchase_count = models.PositiveIntegerField(default=1) 

    def __str__(self):
        return f'Purchase of {self.book.title} by {self.user.username}'

