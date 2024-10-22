from django.shortcuts import render,get_object_or_404,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.contrib.auth import logout
from django.contrib import messages 
from datetime import datetime
from home.models import Contact
from home.models import Book
from home.forms import BookForm
from django.contrib.auth.decorators import login_required
from home.models import Purchase
from django.core.paginator import Paginator
from home.forms import PurchaseForm
from django.db.models import Q

# Create your views here.
def index(request):
    if request.user.is_anonymous:
        return redirect("/login")
    return render(request , "index.html")



# Register User View


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'book_detail.html', {'book': book})

@login_required
def buy_book(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            # Check if there's an existing purchase for this user and book
            purchases = Purchase.objects.filter(user=request.user, book=book)
            
            if purchases.exists():
                # Update the latest purchase if it exists
                purchase = purchases.latest('purchased_at')  # Get the most recent purchase
                purchase.purchase_count += 1
                purchase.name = form.cleaned_data['name']
                purchase.email = form.cleaned_data['email']
                purchase.phone_number = form.cleaned_data['phone_number']
                purchase.address = form.cleaned_data['address']
                purchase.save()
                messages.info(request, f'You have bought this book {purchase.purchase_count} times.')
            else:
                # Create a new purchase if none exist
                purchase = form.save(commit=False)  # Avoid saving the form directly
                purchase.user = request.user  # Associate with the logged-in user
                purchase.book = book
                purchase.purchase_count = 1  # Since it's the first purchase
                purchase.save()
                messages.success(request, 'You have successfully bought this book.')

            return redirect('success_page')  # Redirect to a success page or another view
    else:
        form = PurchaseForm()

    return render(request, 'buy_book.html', {'book': book, 'form': form})

@login_required
def sell_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.seller = request.user
            book.save()
            messages.success(request, 'Your book has been listed for sale successfully!')
            return redirect('book_detail', pk=book.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BookForm()
    return render(request, 'sell_book.html', {'form': form})

def book_list(request):
    query = request.GET.get('q')  # Get the search term from the query parameters
    if query:
        # Filter books based on the search query, searching by title and author
        book_list = Book.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        )
    else:
        # If no search query, display all books
        book_list = Book.objects.all()
    
    paginator = Paginator(book_list, 10)  # Show 10 books per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Pass the query back to the template for display in the search box
    return render(request, 'book_list.html', {'page_obj': page_obj, 'query': query})

def success_page(request):
    return render(request, 'success.html') 
