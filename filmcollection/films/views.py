from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from api.kinopoisk.api_kinopisk import get_films, get_film_from_id, recommended_films
from .models import Film, WatchedFilm, Favorite, Deferred, User


def paginator(queryset, request):
    paginator = Paginator(queryset, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return {'page_obj': page_obj}


def get_films_data(request, films):
    films_list = []
    films_watched = (Film.objects.filter(watched_film__user=request.user))
    films_favorites = (Film.objects.filter(favorite__user=request.user))
    films_deferreds = (Film.objects.filter(deferred__user=request.user))
    for res in films:
        if res in films_favorites:
            favorite = True
        else:
            favorite = False
        if res in films_watched:
            watched = True
        else:
            watched = False
        if res in films_deferreds:
            deferred = True
        else:
            deferred = False
        film = {}
        film = {
            'film_id': res.film_id,
            'name_ru': res.name_ru,
            'name_en': res.name_en,
            'year': res.year,
            'description': res.description,
            'film_length': res.film_length,
            # 'genres': res.genres,
            # 'user_rating': range(res.watched_film.get(film=res).rating),
            'name_original': res.name_original,
            'rating': res.rating,
            'image': res.image,
            'favorite': favorite,
            'watched': watched,
            'deferred': deferred,
        }
        rating = res.watched_film.filter(film=res)
        if rating.exists():
            rating = rating[0]
            film.update({'user_rating': range(rating.rating)})
        films_list.append(film)
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
             order_by('-watched_film__pub_date'))
    context = get_films_data(request, films)
    return render(request, template_name='films/films_watched.html', context=context)


@login_required
def favorite_films(request):
    films = (Film.objects.
             filter(favorite__user=request.user).
             order_by('-favorite__pub_date'))
    context = get_films_data(request, films)
    return render(request, template_name='films/films_favorites.html', context=context)


@login_required
def deferred_films(request):
    films = (Film.objects.
             filter(deferred__user=request.user).
             order_by('-deferred__pub_date'))
    context = get_films_data(request, films)
    return render(request, template_name='films/deferred_films.html', context=context)


def search(request):
    query = request.GET.get('res')
    if query == '':
        return redirect(to='films:index')
    result = get_films(query)
    page_obj = paginator(result, request)
    context = dict()
    context.update(page_obj)
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
    film_obj = Film.objects.prefetch_related('watched_film', 'favorite', 'deferred').get(film_id=film_id)
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
        WatchedFilm.objects.create(user=request.user, film=film_obj, rating=user_rating)
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


def get_recommended_films(request):
    random_favorite_films = Favorite.objects.select_related('film').filter(user=request.user).order_by('?')
    user_watched_films = Film.objects.filter(watched_film__user=request.user)
    user_favorite_films = Film.objects.filter(favorite__user=request.user)
    film_list = []
    for film in random_favorite_films:
        film_list.append(film.film.film_id)
        if len(film_list) == 5:
            break
    recommended = recommended_films(film_list)
    print(recommended)
    return render(request, template_name='films/recommended_films.html')