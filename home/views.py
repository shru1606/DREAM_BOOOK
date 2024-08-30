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

def about(request):
    return render(request , "about.html")

# Register User View
def registeruser(request):
    if request.method == "POST":
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        
        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return render(request, "register.html")
        
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return render(request, "register.html")
        if User.objects.filter(email=email).exists():
            messages.error(request, "email already exists!")
            return render(request, "register.html")

        # Create a new user
        user = User.objects.create_user(email=email ,username=username, password=password)
        user.save()
        messages.success(request, "Registration successful! Please log in.")
        return redirect("/login")  # Redirect to login page after successful registration
    
    return render(request, "register.html")
    
def loginuser(request):
    if request.method=="POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request , user)
    # A backend authenticated the credentials
            return redirect("/")
        else:
            # No backend authenticated the credentials
            messages.error(request, "Invalid username or password")
            return render(request , "login.html")


    return render(request , "login.html")
    
def logoutuser(request):
    logout(request)
    return redirect("/login")

def contact(request):
    if request.method=="POST":
        name= request.POST.get('name')
        email= request.POST.get('email')
        phone= request.POST.get('phone')
        desc= request.POST.get('desc')
        contact = Contact(name=name , email=email , phone=phone ,desc=desc , date= datetime.today() )
        contact.save()
        messages.success(request, "contacts details updated.")
        
    return render(request , "contact.html" )

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
