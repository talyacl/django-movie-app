from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.

from django.contrib.auth import login as auth_login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Movie, Watchlist
from django.conf import settings
from django.contrib import messages
import requests

def search_movies(request):
    query = request.GET.get('q')
    if query:
        response = requests.get(f'https://api.themoviedb.org/3/search/movie?api_key={settings.TMDB_API_KEY}&query={query}')
        movies = response.json().get('results', [])
    else:
        movies = []
    return render(request, 'base/search_movies.html', {'movies': movies})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('view_watchlist')
    else:
        form = UserCreationForm()
    return render(request, 'base/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('view_watchlist')
    else:
        form = AuthenticationForm()
    return render(request, 'base/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def add_to_watchlist(request, tmdb_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={settings.TMDB_API_KEY}')
    data = response.json()
    
    movie, created = Movie.objects.get_or_create(
        tmdb_id=tmdb_id,
        defaults={
            'title': data['title'],
            'overview': data['overview'],
            'poster_path': data['poster_path'],
            'release_date': data['release_date'],
        }
    )
    
    Watchlist.objects.get_or_create(user=request.user, movie=movie)
    return redirect('view_watchlist')

@login_required
def view_watchlist(request):
    watchlist = Watchlist.objects.filter(user=request.user)
    return render(request, 'base/view_watchlist.html', {'watchlist': watchlist})


def get_popular_movies():
    api_key = settings.TMDB_API_KEY
    url = f'https://api.themoviedb.org/3/movie/popular?api_key={api_key}&language=en-US&page=1'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('results', [])
    return []

def home(request):
    popular_movies = get_popular_movies()
    return render(request, 'base/home.html', {'popular_movies': popular_movies})

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    return render(request, 'base/movie_detail.html', {'movie': movie})


@login_required
def remove_from_watchlist(request, tmdb_id):
    movie = get_object_or_404(Movie, tmdb_id=tmdb_id)
    
    watchlist_item = Watchlist.objects.filter(user=request.user, movie=movie).first()
    
    if watchlist_item:
        watchlist_item.delete()
        messages.success(request, 'Movie removed from watchlist successfully.')
    else:
        messages.error(request, 'Movie not found in your watchlist.')
    
    return redirect('movie_detail', movie_id=movie.id)
