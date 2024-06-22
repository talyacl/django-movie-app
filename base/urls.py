from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search_movies, name='search_movies'),
    path('add/<int:tmdb_id>/', views.add_to_watchlist, name='add_to_watchlist'),
    path('watchlist/', views.view_watchlist, name='view_watchlist'),
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('remove/<int:tmdb_id>/', views.remove_from_watchlist, name='remove_from_watchlist'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='base/login.html'), name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
]
