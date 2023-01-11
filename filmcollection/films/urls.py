from django.urls import path

from . import views


app_name = 'films'

urlpatterns = [
    path('favorite/', views.favorite_films, name='favorite_films'),
    path('watched/', views.watched_films, name='watched_films'),
    path('deferred/', views.deferred_films, name='deferred_films'),
    path('search/', views.search, name='search'),
    path('add_film_to_watched/<int:film_id>/', views.add_film_to_watched, name='watched_film'),
    path('', views.index, name='index'),
]
