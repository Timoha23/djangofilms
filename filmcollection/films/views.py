from django.shortcuts import render, redirect
from api.kinopoisk.api_kinopisk import get_films, get_film_from_id


def index(request):
    return render(request, template_name='films/index.html')


def watched_films(request):
    return render(request, template_name='films/films_watched.html')


def favorite_films(request):
    return render(request, template_name='films/films_favorites.html')


def deferred_films(request):
    return render(request, template_name='films/deferred_films.html')


def search(request):
    query = request.GET.get('res')
    if query == '':
        return redirect(to='films:index')
    result = get_films(query)
    context = {
        'films': result,
        'query': query,
    }
    return render(request, template_name='films/search_result.html', context=context)


def add_film_to_watched(request, film_id):
    film = get_film_from_id(film_id)
    context = {
        'film': film,
    }
    return render(request, template_name='films/add_film_to_watched.html', context=context)
