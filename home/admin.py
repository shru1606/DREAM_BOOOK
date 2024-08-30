from django.contrib import admin
from home.models import Contact
from home.models import Book,Purchase
# Register your models here.
# Register models only once
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'desc', 'date')
    search_fields = ('name', 'email')

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'price', 'seller', 'created_at')
    search_fields = ('title', 'author')

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'purchased_at')
    search_fields = ('user__username', 'book__title')