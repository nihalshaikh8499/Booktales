"""
URL configuration for Booktales project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('tales_list/', views.tales_list, name = 'tales_list'),
    path('create/', views.tales_create, name = 'tales_create'),
    path('<int:tale_id>/edit/', views.tales_edit, name = 'tales_edit'),
    path('<int:tale_id>/delete/', views.tales_delete, name = 'tales_delete'),
    path('register/',views.register, name = 'register'),
    path('<int:tale_id>/', views.tale_detail, name='tale_detail'),
    path('books/search/', views.book_search, name='book_search'),
    path('tales/create/<str:book_id>/', views.tale_create_from_book, name='tale_create_from_book'),
    path('tales_user_list/',views.tales_user_list, name = 'tales_user_list'),
    path('bookmark',views.bookmark_tale, name = 'bookmark'),
    path('bookmarked_list/',views.bookmarked_list,name='bookmarked_list')
] 
