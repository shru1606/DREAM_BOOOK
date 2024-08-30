from django import forms
from home.models import Book,Purchase

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'price', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'cols': 80, 'rows': 10}),
            'price': forms.NumberInput(attrs={'step': '0.01'}),
            'image': forms.ClearableFileInput(attrs={'multiple': False}),  # Allows multiple file uploads if needed
        }


class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['name', 'email', 'phone_number', 'address']
        widgets = {
            'address': forms.Textarea(attrs={'cols': 80, 'rows': 5}),
        }