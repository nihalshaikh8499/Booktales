import requests
from django.core.files.base import ContentFile
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from .models import Tales
from .forms import TalesForm, UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
import os 

from django.http import JsonResponse

def index(request):
    return render(request, 'index.html')

def tales_list(request):
    query = request.GET.get('q', '')  
    tales = Tales.objects.all().order_by('-created_at') 

    if query:
        tales = tales.filter(title__icontains=query) 

    return render(request, 'tales_list.html', {'tales': tales, 'query': query})

def bookmarked_list(request): 
    tales = Tales.objects.all().filter(bookmarked_by = request.user).order_by('-created_at')

    return render(request, 'bookmarked_list.html', {'tales': tales})

@login_required
def tales_user_list(request):
    tales = Tales.objects.filter(user=request.user).order_by('-created_at')  

    return render(request, 'tales_user_list.html', {'tales': tales})

@login_required
def tales_create(request):
    """View for creating a new tale with prefilled book data."""
    book_id = request.GET.get('book_id')  # Get book ID from the query string
    book = {'title': 'Untitled', 'cover_url': None}  # Default empty book data with a title

    if book_id:
        # Fetch book details using Open Library API
        api_url = f"https://openlibrary.org{book_id}.json"
        response = requests.get(api_url)

        if response.status_code == 200:
            try:
                data = response.json()
                book['title'] = data.get('title', 'Untitled')  # Safely get title
                cover_id = data.get('covers', [None])[0]  # Safely get cover ID
                book['cover_url'] = f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg" if cover_id else None
            except ValueError:
                # Handle error if JSON response is invalid
                book['error'] = "Invalid book data received from Open Library."
        else:
            book['error'] = "Error fetching book data from Open Library."

    if request.method == 'POST':
        form = TalesForm(request.POST, request.FILES)
        if form.is_valid():
            tale = form.save(commit=False)
            tale.user = request.user  # Set the logged-in user

            # If a cover URL is available, download and save the image
            if book.get('cover_url'):
                try:
                    # Ensure the URL is safe and doesn't cause path traversal
                    image_response = requests.get(book['cover_url'])
                    if image_response.status_code == 200:
                        # Generate a safe filename
                        cover_filename = os.path.basename(book['cover_url'])
                        safe_name = cover_filename.replace('/', '_')  # Replace any invalid path characters
                        
                        # Save the image
                        tale.photo.save(safe_name, ContentFile(image_response.content), save=True)

                except requests.RequestException as e:
                    # Handle any error that occurs during image download
                    tale.photo = None  # Set photo to None if image download fails

            tale.save()  # Save the tale instance
            return redirect('tales_list')

    else:
        form = TalesForm(initial={'title': book.get('title', 'Untitled')})

    return render(request, 'tales_form.html', {'form': form, 'book': book})

@login_required
def tales_edit(request, tale_id):
    book = get_object_or_404(Tales, pk=tale_id, user=request.user)

    if request.method == 'POST':
        form = TalesForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            book = form.save(commit=False)
            book.user = request.user
            book.save()
            return redirect('tales_list')
    else:
        form = TalesForm(instance=book)

    # Include 'tale' in the context
    return render(request, 'tales_form.html', {'form': form, 'book': book})

@login_required
def  tales_delete(request, tale_id):
    tale = get_object_or_404(Tales, pk = tale_id, user = request.user)
    if request.method == 'POST':
        tale.delete()
        return redirect('tales_list')
    return render(request, 'tales_confirm_delete.html',{'tale':tale})

def tale_detail(request, tale_id):
    tale = get_object_or_404(Tales, id=tale_id)
    
    return render(request, 'tale_detail.html', {'tale': tale})

def book_search(request):
    query = request.GET.get('q', '')
    books = []
    
    if query:
        api_url = f"https://openlibrary.org/search.json"
        params = {"q": query, "limit": 10}
        response = requests.get(api_url, params=params)
        
        if response.status_code == 200:
            results = response.json().get('docs', [])
            for item in results:
                books.append({
                    'key': item.get('key'),
                    'title': item.get('title'),
                    'author_name': item.get('author_name', []),
                    'cover_i': item.get('cover_i'),
                })

    return render(request, 'book_search.html', {'books': books, 'query': query})

@login_required
def tale_create_from_book(request, book_id):
    """Prefill tale creation form with book data."""
    # Fetch book details using Open Library API
    api_url = f"https://openlibrary.org{book_id}.json"
    response = requests.get(api_url)
    book = {}

    if response.status_code == 200:
        data = response.json()
        book['title'] = data.get('title', '')
        cover_url = f"https://covers.openlibrary.org/b/id/{data.get('covers', [])[0]}-L.jpg" if data.get('covers') else None
        book['cover_url'] = cover_url

    if request.method == 'POST':
        form = TalesForm(request.POST, request.FILES)
        if form.is_valid():
            tale = form.save(commit=False)
            tale.user = request.user

            # If a cover URL is available, save the image
            if book['cover_url']:
                image_response = requests.get(book['cover_url'])
                if image_response.status_code == 200:
                    image_name = f"{book_id}_cover.jpg"
                    tale.photo.save(image_name, ContentFile(image_response.content), save=True)

            tale.title = book['title']  # Set the title from the book data
            tale.save()
            return redirect('tales_list')
    else:
        form = TalesForm(initial={'title': book['title']})

    return render(request, 'tales_form.html', {'form': form, 'book': book})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('tales_list')
    else:
        form = UserRegistrationForm()

    return render(request, 'registration/register.html',{'form':form})

@login_required
def bookmark_tale(request):
    tale_id = request.POST.get('tale_id')
    tale = get_object_or_404(Tales, id=tale_id)

    if tale.bookmarked_by.filter(id=request.user.id).exists():
        tale.bookmarked_by.remove(request.user)
        bookmarked = False
    else:
        tale.bookmarked_by.add(request.user)
        bookmarked = True

    # Get the first user who liked this tale
    first_bookmarker = tale.bookmarked_by.first()
    
    return JsonResponse({
        "bookmarked": bookmarked,
        # "like_count": tale.liked_by.count(),
        # "first_user": first_liker.username if first_liker else "",
        # "first_user_is_me": first_liker == request.user
    })
