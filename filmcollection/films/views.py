from django.shortcuts import render, redirect
from api.kinopoisk.api_kinopisk import get_films, get_film_from_id
from .models import Film, UserRating, User


def index(request):
    return render(request, template_name='films/index.html')


def watched_films(request):
    user_films = UserRating.objects.filter(user=request.user).order_by('-pub_date')
    films_list = []
    for res in user_films:
        film = {}
        film = {
            'film_id': res.film.film_id,
            'name_ru': res.film.name_ru,
            'name_en': res.film.name_en,
            'year': res.film.year,
            'description': res.film.description,
            'film_length': res.film.film_length,
            # 'genres': res.film.genres,
            'name_original': res.film.name_original,
            'rating': res.film.rating,
            'image': res.film.image,
            'user_rating': range(res.rating),
        }
        films_list.append(film)
    context = {
        'films': films_list,
    }
    return render(request, template_name='films/films_watched.html', context=context)


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


def film_page(request, film_id):
    film = get_film_from_id(film_id)
    context = {
        'film': film,
    }
    return render(request, template_name='films/film.html', context=context)


def add_film_to_watched(request, film_id):
    if request.POST.get('rating') is None:
        return redirect(to='films:index')
    film = get_film_from_id(film_id)
    user_rating = int(request.POST['rating'])
    if Film.objects.filter(film_id=film_id).exists() is False:
        Film.objects.create(
            film_id=film_id,
            name_ru=film.get('name_ru'),
            name_en=film.get('name_en'),
            name_original=film.get('name_original'),
            year=film.get('year'),
            description=film.get('description'),
            film_length=film.get('film_length'),
            rating=film.get('rating'),
            image=film.get('image')
        )
    film_obj = Film.objects.get(film_id=film_id)
    if UserRating.objects.filter(user=request.user, film=film_obj):
        UserRating.objects.update(rating=user_rating)
    else:
        UserRating.objects.create(user=request.user, film=film_obj, rating=user_rating)
    return redirect(to='films:watched_films')
