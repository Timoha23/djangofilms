from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from api.kinopoisk.api_kinopisk import get_films, get_film_from_id
from .models import Film, WatchedFilm, User, Favorite, Deferred


def index(request):
    return render(request, template_name='films/index.html')


@login_required
def watched_films(request):
    films = (Film.objects.
             filter(watched_film__user=request.user).
             order_by('-watched_film__pub_date'))
    # films_rating = (Film.objects.
    #                 filter(watched_film__user=request.user).
    #                 order_by('-watched_film__pub_date').
    #                 values('watched_film__rating'))
    films_favorites = (Film.objects.filter(favorite__user=request.user))
    films_deferreds = (Film.objects.filter(deferred__user=request.user))
    films_list = []
    # index = 0
    for res in films:
        if res in films_deferreds:
            deferred = True
        else:
            deferred = False
        if res in films_favorites:
            favorite = True
        else:
            favorite = False
        film = {}
        # rating = films_rating[index]
        film = {
            'film_id': res.film_id,
            'name_ru': res.name_ru,
            'name_en': res.name_en,
            'year': res.year,
            'description': res.description,
            'film_length': res.film_length,
            # 'genres': res.genres,
            'name_original': res.name_original,
            'rating': res.rating,
            'image': res.image,
            'user_rating': range(res.watched_film.get(film=res).rating),
            'watched': True,
            'favorite': favorite,
            'deferred': deferred,
        }
        # index += 1
        films_list.append(film)
    context = {
        'films': films_list,
    }
    return render(request, template_name='films/films_watched.html', context=context)


@login_required
def favorite_films(request):
    films = (Film.objects.
             filter(favorite__user=request.user).
             order_by('-favorite__pub_date'))
    films_list = []
    films_watched = (Film.objects.filter(watched_film__user=request.user))
    films_deferreds = (Film.objects.filter(deferred__user=request.user))
    for res in films:
        if res in films_deferreds:
            deferred = True
        else:
            deferred = False
        if res in films_watched:
            watched = True
        else:
            watched = False
        film = {}
        film = {
            'film_id': res.film_id,
            'name_ru': res.name_ru,
            'name_en': res.name_en,
            'year': res.year,
            'description': res.description,
            'film_length': res.film_length,
            # 'genres': res.genres,
            'name_original': res.name_original,
            'rating': res.rating,
            'image': res.image,
            'deferred': deferred,
            'favorite': True,
            'watched': watched,
        }
        films_list.append(film)
    context = {
        'films': films_list,
    }
    return render(request, template_name='films/films_favorites.html', context=context)


@login_required
def deferred_films(request):
    films = (Film.objects.
             filter(deferred__user=request.user).
             order_by('-deferred__pub_date'))
    films_list = []
    films_watched = (Film.objects.filter(watched_film__user=request.user))
    films_favorites = (Film.objects.filter(favorite__user=request.user))
    for res in films:
        if res in films_favorites:
            favorite = True
        else:
            favorite = False
        if res in films_watched:
            watched = True
        else:
            watched = False
        film = {}
        film = {
            'film_id': res.film_id,
            'name_ru': res.name_ru,
            'name_en': res.name_en,
            'year': res.year,
            'description': res.description,
            'film_length': res.film_length,
            # 'genres': res.genres,
            'name_original': res.name_original,
            'rating': res.rating,
            'image': res.image,
            'favorite': favorite,
            'watched': watched,
            'deferred': True,
        }
        films_list.append(film)
    context = {
        'films': films_list,
    }
    return render(request, template_name='films/deferred_films.html', context=context)


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


@login_required
def film_page(request, film_id):
    film = get_film_from_id(film_id)
    if Film.objects.filter(film_id=film_id).exists() is False:
        context = {
            'film': film,
            'favorite': False,
            'watched': False,
            'deferred': False,
        }
        return render(request, template_name='films/film.html', context=context)
    film_obj = Film.objects.get(film_id=film_id)
    film_watched = WatchedFilm.objects.filter(film=film_obj, user=request.user).exists()
    film_favorite = Favorite.objects.filter(film=film_obj, user=request.user).exists()
    film_deferred = Deferred.objects.filter(film=film_obj).exists()
    context = {
        'film': film,
        'favorite': film_favorite,
        'watched': film_watched,
        'deferred': film_deferred,
    }
    return render(request, template_name='films/film.html', context=context)


@login_required
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
    if WatchedFilm.objects.filter(user=request.user, film=film_obj):
        WatchedFilm.objects.update(rating=user_rating)
    else:
        WatchedFilm.objects.create(user=request.user, film=film_obj, rating=user_rating)
    return redirect(to='films:watched_films')


@login_required
def delete_film_from_watched(request, film_id):
    # film = get_film_from_id(film_id)
    # if Film.objects.filter(film_id=film_id).exists() is False:
    #     Film.objects.create(
    #         film_id=film_id,
    #         name_ru=film.get('name_ru'),
    #         name_en=film.get('name_en'),
    #         name_original=film.get('name_original'),
    #         year=film.get('year'),
    #         description=film.get('description'),
    #         film_length=film.get('film_length'),
    #         rating=film.get('rating'),
    #         image=film.get('image')
    #     )
    film_obj = Film.objects.get(film_id=film_id)
    WatchedFilm.objects.filter(
        film=film_obj,
        user=request.user
    ).delete()
    return redirect(to='films:watched_films')


@login_required
def add_film_to_favorite(request, film_id):
    film = get_film_from_id(film_id)
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
    Favorite.objects.create(
        film=film_obj,
        user=request.user,
    )
    return redirect(to='films:favorite_films')


@login_required
def delete_film_from_favorite(request, film_id):
    # film = get_film_from_id(film_id)
    # if Film.objects.filter(film_id=film_id).exists() is False:
    #     Film.objects.create(
    #         film_id=film_id,
    #         name_ru=film.get('name_ru'),
    #         name_en=film.get('name_en'),
    #         name_original=film.get('name_original'),
    #         year=film.get('year'),
    #         description=film.get('description'),
    #         film_length=film.get('film_length'),
    #         rating=film.get('rating'),
    #         image=film.get('image')
    #     )
    film_obj = Film.objects.get(film_id=film_id)
    Favorite.objects.filter(
        film=film_obj,
        user=request.user
    ).delete()
    return redirect(to='films:favorite_films')


@login_required
def add_film_to_deferred(request, film_id):
    film = get_film_from_id(film_id)
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
    Deferred.objects.create(
        film=film_obj,
        user=request.user,
    )
    return redirect(to='films:deferred_films')


@login_required
def delete_film_from_deferred(request, film_id):
    # film = get_film_from_id(film_id)
    # if Film.objects.filter(film_id=film_id).exists() is False:
    #     Film.objects.create(
    #         film_id=film_id,
    #         name_ru=film.get('name_ru'),
    #         name_en=film.get('name_en'),
    #         name_original=film.get('name_original'),
    #         year=film.get('year'),
    #         description=film.get('description'),
    #         film_length=film.get('film_length'),
    #         rating=film.get('rating'),
    #         image=film.get('image')
    #     )
    film_obj = Film.objects.get(film_id=film_id)
    Deferred.objects.filter(
        film=film_obj,
        user=request.user
    ).delete()
    return redirect(to='films:deferred_films')
