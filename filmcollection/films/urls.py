from django.urls import path

from . import views


app_name = 'films'

urlpatterns = [
    path('favorite/', views.favorite_films, name='favorite_films'),
    path('watched/', views.watched_films, name='watched_films'),
    path('deferred/', views.deferred_films, name='deferred_films'),
    path('search/', views.search, name='search'),
    path('film/<int:film_id>/', views.film_page, name='film'),
    path('add_film_to_watched/<int:film_id>/', views.add_film_to_watched, name='watched_film'),
    path('del_film_to_watched/<int:film_id>/', views.delete_film_from_watched, name='delete_watched_film'),
    path('add_film_to_favorite/<int:film_id>/', views.add_film_to_favorite, name='add_favorite'),
    path('del_film_from_favorite/<int:film_id>/', views.delete_film_from_favorite, name='delete_favorite'),
    path('add_film_to_deferred/<int:film_id>/', views.add_film_to_deferred, name='add_deferred'),
    path('del_film_from_deferred/<int:film_id>/', views.delete_film_from_deferred, name='delete_deferred'),
    path('recommendation/', views.get_recommended_films, name='get_recommended'),
    path('error/', views.error_api_page, name='error_api'),
    path('', views.index, name='index'),
]
