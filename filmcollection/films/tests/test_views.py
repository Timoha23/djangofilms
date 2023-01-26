from django.test import Client, TestCase
from django.urls import reverse

from ..models import User, Film, Favorite, WatchedFilm, Deferred
from ..views import get_film_obj


FILM_ID = 685246
USER_RATING = 3


class FilmsPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Добавляем юзера 1
        cls.user_1 = User.objects.create_user(username='user_1')
        cls.auth_user_1 = Client()
        cls.auth_user_1.force_login(cls.user_1)

        # Добавляем юзера 2
        cls.user_2 = User.objects.create_user(username='user_2')
        cls.auth_user_2 = Client()
        cls.auth_user_2.force_login(cls.user_2)

        cls.watched_film_user_1 = WatchedFilm.objects.create(
            film=get_film_obj(FILM_ID),
            user=cls.user_1,
            rating=USER_RATING,
        )

        cls.favorite_film_user_1 = Favorite.objects.create(
            film=get_film_obj(FILM_ID),
            user=cls.user_1,
        )

        cls.deferred_film_user_1 = Deferred.objects.create(
            film=get_film_obj(FILM_ID),
            user=cls.user_1,
        )

    def test_views_correct_templates(self):
        """Проверка вью на корректность используемых шаблонов"""

        views_templates_names = {
            reverse('films:index'): 'films/index.html',
            reverse('films:favorite_films'): 'films/films_favorites.html',
            reverse('films:watched_films'): 'films/films_watched.html',
            reverse('films:deferred_films'): 'films/deferred_films.html',
            reverse('films:search'): 'films/search_result.html',
            reverse('films:film', kwargs={'film_id': FILM_ID}): 'films/film.html',
            reverse('films:error_api'): 'films/error_api.html',
            reverse('films:get_recommended'): 'films/recommended_films.html',


        }

        for view, template in views_templates_names.items():
            with self.subTest(template=template):
                response = self.auth_user_1.get(view)
                self.assertTemplateUsed(response, template)

    def test_watched_films_correct_context(self):
        """Шаблон watched сформирован с правильным контекстом"""

        response = self.auth_user_1.get(reverse('films:watched_films'))
        len_response = len(response.context['page_obj'])
        film_object = response.context['page_obj'][0]

        film_id = film_object.get('film_id')
        name_ru = film_object.get('name_ru')
        name_en = film_object.get('name_en')
        year = film_object.get('year')
        description = film_object.get('description')
        film_length = film_object.get('film_length')
        name_original = film_object.get('name_original')
        rating = film_object.get('rating')
        image = film_object.get('image')
        favorite = film_object.get('favorite')
        watched = film_object.get('watched')
        deferred = film_object.get('deferred')
        user_rating = film_object.get('user_rating')

        self.assertEqual(
            len_response, WatchedFilm.objects.filter(user=self.user_1).count()
        )
        self.assertEqual(film_id, self.watched_film_user_1.film.film_id)
        self.assertEqual(name_ru, self.watched_film_user_1.film.name_ru)
        self.assertEqual(name_en, self.watched_film_user_1.film.name_en)
        self.assertEqual(year, self.watched_film_user_1.film.year)
        self.assertEqual(description, self.watched_film_user_1.film.description)
        self.assertEqual(film_length, self.watched_film_user_1.film.film_length)
        self.assertEqual(name_original, self.watched_film_user_1.film.name_original)
        self.assertEqual(rating, self.watched_film_user_1.film.rating)
        self.assertEqual(image, self.watched_film_user_1.film.image)
        self.assertEqual(favorite, self.watched_film_user_1.film.favorite.exists())
        self.assertEqual(watched, self.watched_film_user_1.film.watched_film.exists())
        self.assertEqual(deferred, self.watched_film_user_1.film.deferred.exists())
        self.assertEqual(user_rating.stop, self.watched_film_user_1.rating)

    def test_favorite_films_correct_context(self):
        """Шаблон favorite сформирован с правильным контекстом"""

        response = self.auth_user_1.get(reverse('films:favorite_films'))
        len_response = len(response.context['page_obj'])
        film_object = response.context['page_obj'][0]

        film_id = film_object.get('film_id')
        name_ru = film_object.get('name_ru')
        name_en = film_object.get('name_en')
        year = film_object.get('year')
        description = film_object.get('description')
        film_length = film_object.get('film_length')
        name_original = film_object.get('name_original')
        rating = film_object.get('rating')
        image = film_object.get('image')
        favorite = film_object.get('favorite')
        watched = film_object.get('watched')
        deferred = film_object.get('deferred')
        user_rating = film_object.get('user_rating')

        self.assertEqual(
            len_response, Favorite.objects.filter(user=self.user_1).count()
        )
        self.assertEqual(film_id, self.favorite_film_user_1.film.film_id)
        self.assertEqual(name_ru, self.favorite_film_user_1.film.name_ru)
        self.assertEqual(name_en, self.favorite_film_user_1.film.name_en)
        self.assertEqual(year, self.favorite_film_user_1.film.year)
        self.assertEqual(description, self.favorite_film_user_1.film.description)
        self.assertEqual(film_length, self.favorite_film_user_1.film.film_length)
        self.assertEqual(name_original, self.favorite_film_user_1.film.name_original)
        self.assertEqual(rating, self.favorite_film_user_1.film.rating)
        self.assertEqual(image, self.favorite_film_user_1.film.image)
        self.assertEqual(favorite, self.favorite_film_user_1.film.favorite.exists())
        self.assertEqual(watched, self.favorite_film_user_1.film.watched_film.exists())
        self.assertEqual(deferred, self.favorite_film_user_1.film.deferred.exists())
        self.assertEqual(user_rating.stop, self.watched_film_user_1.rating)

    def test_deferred_films_correct_context(self):
        """Шаблон deferred сформирован с правильным контекстом"""

        response = self.auth_user_1.get(reverse('films:deferred_films'))
        len_response = len(response.context['page_obj'])
        film_object = response.context['page_obj'][0]

        film_id = film_object.get('film_id')
        name_ru = film_object.get('name_ru')
        name_en = film_object.get('name_en')
        year = film_object.get('year')
        description = film_object.get('description')
        film_length = film_object.get('film_length')
        name_original = film_object.get('name_original')
        rating = film_object.get('rating')
        image = film_object.get('image')
        favorite = film_object.get('favorite')
        watched = film_object.get('watched')
        deferred = film_object.get('deferred')
        user_rating = film_object.get('user_rating')

        self.assertEqual(
            len_response, Deferred.objects.filter(user=self.user_1).count()
        )
        self.assertEqual(film_id, self.deferred_film_user_1.film.film_id)
        self.assertEqual(name_ru, self.deferred_film_user_1.film.name_ru)
        self.assertEqual(name_en, self.deferred_film_user_1.film.name_en)
        self.assertEqual(year, self.deferred_film_user_1.film.year)
        self.assertEqual(description, self.deferred_film_user_1.film.description)
        self.assertEqual(film_length, self.deferred_film_user_1.film.film_length)
        self.assertEqual(name_original, self.deferred_film_user_1.film.name_original)
        self.assertEqual(rating, self.deferred_film_user_1.film.rating)
        self.assertEqual(image, self.deferred_film_user_1.film.image)
        self.assertEqual(favorite, self.deferred_film_user_1.film.favorite.exists())
        self.assertEqual(watched, self.deferred_film_user_1.film.watched_film.exists())
        self.assertEqual(deferred, self.deferred_film_user_1.film.deferred.exists())
        self.assertEqual(user_rating.stop, self.watched_film_user_1.rating)

    def test_search_correct_context(self):
        """Шаблон search сформирован с правильным контекстом"""
        ...

    def test_film_page_correct_context(self):
        """Шаблон film_page сформирован с правильным контекстом"""
        response = self.auth_user_1.get(reverse('films:film', kwargs={'film_id': FILM_ID}))
        film = get_film_obj(FILM_ID)
        film_on_page = response.context['film']

        film_id = film_on_page.get('film_id')
        name_ru = film_on_page.get('name_ru')
        name_en = film_on_page.get('name_en')
        year = film_on_page.get('year')
        description = film_on_page.get('description')
        film_length = film_on_page.get('film_length')
        name_original = film_on_page.get('name_original')
        rating = film_on_page.get('rating')
        image = film_on_page.get('image')
        favorite = response.context['favorite']
        watched = response.context['watched']
        deferred = response.context['deferred']
        user_rating = film_on_page.get('user_rating')

        self.assertEqual(film_id, film.film_id)
        self.assertEqual(name_ru, film.name_ru)
        self.assertEqual(name_en, film.name_en)
        self.assertEqual(year, film.year)
        self.assertEqual(description, film.description)
        self.assertEqual(film_length, film.film_length)
        self.assertEqual(name_original, film.name_original)
        self.assertEqual(rating, float(film.rating))
        self.assertEqual(image, film.image)
        self.assertEqual(favorite, Favorite.objects.filter(film=film, user=self.user_1).exists())
        self.assertEqual(watched, WatchedFilm.objects.filter(film=film, user=self.user_1).exists())
        self.assertEqual(deferred, Deferred.objects.filter(film=film, user=self.user_1).exists())
        self.assertEqual(user_rating.stop, self.watched_film_user_1.rating)

    def test_recommended_films_correct_context(self):
        """Шаблон recommended сформирован с правильным контекстом"""
        ...
