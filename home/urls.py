from django.contrib import admin
from django.urls import path,include
from home import views
from django.conf import settings
from django.conf.urls.static import static
from home.views import success_page


urlpatterns = [
    path("" , views.index, name="home"),
    path("login" , views.loginuser, name="login"),
    path('register/', views.registeruser, name='register'),
    path("logout" , views.logoutuser, name="logout"),
    path("contact" , views.contact , name ="contact"),
    path("about" , views.about , name ="about"),
     path('books/', views.book_list, name='book_list'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('buy/<int:pk>/', views.buy_book, name='buy_book'),
    path('sell/', views.sell_book, name='sell_book'),
    path('success/', success_page, name='success_page'), 
    
       
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
