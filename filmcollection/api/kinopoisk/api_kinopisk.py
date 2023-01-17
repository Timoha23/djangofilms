from kinopoisk_unofficial.kinopoisk_api_client import KinopoiskApiClient
from kinopoisk_unofficial.request.films.film_request import FilmRequest
from kinopoisk_unofficial.request.films.search_by_keyword_request import SearchByKeywordRequest
from kinopoisk_unofficial.request.films.related_film_request import RelatedFilmRequest
import random


def get_films(film_name):
    api_client = KinopoiskApiClient("9d4b2df7-f721-490e-95e5-861f111129a0")
    request = SearchByKeywordRequest(film_name)
    response = api_client.films.send_search_by_keyword_request(request)
    films = response.films
    films_list = []
    for res in films:
        film = {}
        film = {
            'film_id': res.film_id,
            'name_ru': res.name_ru,
            'name_en': res.name_en,
            'year': res.year,
            'description': res.description,
            'film_length': res.film_length,
            # 'genres': res.genres,
            'rating': res.rating,
            'image': res.poster_url_preview,
        }
        films_list.append(film)
    return films_list


def get_film_from_id(film_id):
    api_client = KinopoiskApiClient("9d4b2df7-f721-490e-95e5-861f111129a0")
    request = FilmRequest(film_id)
    response = api_client.films.send_film_frame_request(request)
    result = response.film
    film = {
            'film_id': result.kinopoisk_id,
            'name_ru': result.name_ru,
            'name_en': result.name_en,
            'name_original': result.name_original,
            'year': result.year,
            'description': result.description,
            'film_length': result.film_length,
            # 'genres': result.genres,
            'rating': result.rating_kinopoisk,
            'image': result.poster_url_preview,
        }
    return film


def recommended_films(film_list):
    films_list = []
    for film in film_list:
        api_client = KinopoiskApiClient("9d4b2df7-f721-490e-95e5-861f111129a0")
        request = RelatedFilmRequest(film)
        response = api_client.films.send_related_film_request(request)
        films = response.items
        for res in films:
            film = {}
            film = {
                'film_id': res.film_id,
                'name_ru': res.name_ru,
                'name_en': res.name_en,
                'name_original': res.name_original,
                'image': res.poster_url_preview,
            }
            films_list.append(film)
    lenght_list = 10 if len(films_list) > 10 else len(films_list)
    result_films_list = random.sample(films_list, lenght_list)
    return result_films_list
