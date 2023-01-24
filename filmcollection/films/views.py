from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from api.kinopoisk.api_kinopisk import get_films, get_film_from_id, recommended_films
from .models import Film, WatchedFilm, Favorite, Deferred, User
import inspect


def check_api_error_decorator(func):
    def wrapper(request, *args, **kwargs):
        try:
            return func(request, *args, **kwargs)
        except Exception as ex:
            print(ex)
            return error_api_page(request)
    return wrapper


def paginator(films: list, request):
    # получаем название функции из которой была вызвана данная функция
    items_on_page = 5
    caller_func = inspect.currentframe().f_back.f_code.co_name
    if caller_func == 'get_recommended_films':
        items_on_page = 10
    paginator = Paginator(films, items_on_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return {'page_obj': page_obj}


def get_films_data(request, films):
    """Получение данных о фильмах для юзера
    Данная функция работает только с фильмами,
    которые уже есть в БД."""

    films_list = []
    films_watched = (Film.objects.filter(watched_film__user=request.user))
    films_favorites = (Film.objects.filter(favorite__user=request.user))
    films_deferreds = (Film.objects.filter(deferred__user=request.user))
    for film in films:
        if film in films_favorites:
            favorite = True
        else:
            favorite = False
        if film in films_watched:
            watched = True
        else:
            watched = False
        if film in films_deferreds:
            deferred = True
        else:
            deferred = False
        film_dct = {
            'film_id': film.film_id,
            'name_ru': film.name_ru,
            'name_en': film.name_en,
            'year': film.year,
            'description': film.description,
            'film_length': film.film_length,
            # 'genres': film.genres,
            # 'user_rating': range(film.watched_film.get(film=res).rating),
            'name_original': film.name_original,
            'rating': film.rating,
            'image': film.image,
            'favorite': favorite,
            'watched': watched,
            'deferred': deferred,
        }
        user_rating = film.watched_film.filter(film=film)
        if user_rating.exists():
            user_rating = user_rating[0]
            film_dct.update({'user_rating': range(user_rating.rating)})
        films_list.append(film_dct)
    context = dict()
    context.update(paginator(films_list, request))
    return context


def get_film_obj(film_id):
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
    return film_obj


def index(request):
    return render(request, template_name='films/index.html')


@login_required
def watched_films(request):
    films = (Film.objects.
             filter(watched_film__user=request.user).
             prefetch_related('watched_film').
             order_by('-watched_film__pub_date'))
    context = get_films_data(request, films)
    return render(request, template_name='films/films_watched.html',
                  context=context)


@login_required
def favorite_films(request):
    films = (Film.objects.
             filter(favorite__user=request.user).
             order_by('-favorite__pub_date'))
    context = get_films_data(request, films)
    return render(request, template_name='films/films_favorites.html',
                  context=context)


@login_required
def deferred_films(request):
    films = (Film.objects.
             filter(deferred__user=request.user).
             order_by('-deferred__pub_date'))
    context = get_films_data(request, films)
    return render(request, template_name='films/deferred_films.html',
                  context=context)


@check_api_error_decorator
def search(request):
    query = request.GET.get('res')
    if query == '':
        return redirect(to='films:index')
    result = get_films(query)

    page_obj = paginator(result, request)
    context = dict()
    context.update(page_obj)
    return render(request, template_name='films/search_result.html',
                  context=context)


@check_api_error_decorator
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
        return render(request, template_name='films/film.html',
                      context=context)

    film_obj = Film.objects.prefetch_related('watched_film', 'favorite',
                                             'deferred').get(film_id=film_id)
    rating = WatchedFilm.objects.filter(film=film_obj, user=request.user)
    if rating.exists():
        rating = rating[0]
        film.update({'user_rating': range(rating.rating)})
    context = {
        'film': film,
        'favorite': film_obj.favorite.filter(user=request.user).exists(),
        'watched': film_obj.watched_film.filter(user=request.user).exists(),
        'deferred': film_obj.deferred.filter(user=request.user).exists(),
    }
    return render(request, template_name='films/film.html', context=context)


@login_required
def add_film_to_watched(request, film_id):
    redirect_page = request.META.get('HTTP_REFERER')
    if request.POST.get('rating') is None:
        return redirect(to='films:index')
    user_rating = int(request.POST['rating'])
    film_obj = get_film_obj(film_id)
    if WatchedFilm.objects.filter(user=request.user, film=film_obj):
        WatchedFilm.objects.update(rating=user_rating)
    else:
        WatchedFilm.objects.create(user=request.user, film=film_obj,
                                   rating=user_rating)
    return redirect(redirect_page)


@login_required
def delete_film_from_watched(request, film_id):
    redirect_page = request.META.get('HTTP_REFERER')
    film_obj = Film.objects.get(film_id=film_id)
    WatchedFilm.objects.filter(
        film=film_obj,
        user=request.user
    ).delete()
    return redirect(redirect_page)


@login_required
def add_film_to_favorite(request, film_id):
    redirect_page = request.META.get('HTTP_REFERER')
    Favorite.objects.create(
        film=get_film_obj(film_id),
        user=request.user,
    )
    return redirect(redirect_page)


@login_required
def delete_film_from_favorite(request, film_id):
    redirect_page = request.META.get('HTTP_REFERER')
    film_obj = Film.objects.get(film_id=film_id)
    Favorite.objects.filter(
        film=film_obj,
        user=request.user
    ).delete()
    return redirect(redirect_page)


@login_required
def add_film_to_deferred(request, film_id):
    redirect_page = request.META.get('HTTP_REFERER')
    Deferred.objects.create(
        film=get_film_obj(film_id),
        user=request.user,
    )
    return redirect(redirect_page)


@login_required
def delete_film_from_deferred(request, film_id):
    redirect_page = request.META.get('HTTP_REFERER')
    film_obj = Film.objects.get(film_id=film_id)
    Deferred.objects.filter(
        film=film_obj,
        user=request.user
    ).delete()
    return redirect(redirect_page)


@check_api_error_decorator
@login_required
def get_recommended_films(request):
    """Получаем рекомендуемые фильмы (десять случайных фильмов)
    Подборка осуществляется на основе избранных фильмов"""

    random_favorite_films = Favorite.objects.select_related('film').filter(user=request.user).order_by('?')
    user_watched_films = Film.objects.filter(watched_film__user=request.user).values('film_id')
    user_favorite_films = Film.objects.filter(favorite__user=request.user).values('film_id')
    user_deferred_films = Film.objects.filter(deferred__user=request.user).values('film_id')
    films_id = []
    result_films_list = []

    # получение ID фильмов из избранного
    for film in random_favorite_films:
        films_id.append(film.film.film_id)
        if len(films_id) == 5:
            break

    recommended = recommended_films(films_id)

    count_films = 0
    for film in recommended:
        if (
            film.get('film_id') in user_watched_films
            or film.get('film_id') in user_favorite_films
            or film.get('film_id') in user_deferred_films
        ):
            continue
        if film in result_films_list:
            continue
        result_films_list.append(film)
        count_films += 1

        if count_films == 10:
            break
    context = dict()
    context.update(paginator(result_films_list, request))
    return render(request, template_name='films/recommended_films.html', context=context)


def error_api_page(request):
    return render(request, template_name='films/error_api.html')
