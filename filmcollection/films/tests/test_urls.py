from http import HTTPStatus

from django.test import Client, TestCase
from ..models import User, Film


class FilmURLSandTemplatesTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.auth_user = User.objects.create_user(username='auth_user')
        cls.guest_client = Client()
        cls.auth_client = Client()

        cls.auth_client.force_login(cls.auth_user)

        cls.film_in_wfd = Film.objects.create(
            film_id=1,
            name_ru='Тест',
            name_en='Test',
            name_original='Test',
            year=1900,
            description='Тестовое описание',
            film_length=100,
            rating='8',
            image=('https://kinopoiskapiunofficial.tech'
                   '/images/posters/kp_small/8033.jpg')
        )

        cls.film = Film.objects.create(
            film_id=2,
            name_ru='Тест_2',
            name_en='Test_2',
            name_original='Test_2',
            year=2000,
            description='Тестовое описание_2',
            film_length=200,
            rating='2',
            image=('https://kinopoiskapiunofficial.tech'
                   '/images/posters/kp_small/8023.jpg')
        )

    def test_uses_correct_urls(self):
        """Проверка корректности перехода по страницам"""
        urls_names_auth = {
            '/': HTTPStatus.OK,
            '/favorite/': HTTPStatus.OK,
            '/watched/': HTTPStatus.OK,
            '/deferred/': HTTPStatus.OK,
            f'/film/{self.film.id}/': HTTPStatus.OK,
            '/recommendation/': HTTPStatus.OK,
            '/search/': HTTPStatus.OK,
            '/error/': HTTPStatus.OK,
        }

        urls_names_not_auth = {
            '/': HTTPStatus.OK,
            '/favorite/': HTTPStatus.FOUND,
            '/watched/': HTTPStatus.FOUND,
            '/deferred/': HTTPStatus.FOUND,
            f'/film/{self.film.id}/': HTTPStatus.FOUND,
            '/recommendation/': HTTPStatus.FOUND,
            '/search/': HTTPStatus.OK,
            '/error/': HTTPStatus.OK,
        }

        for urls, status in urls_names_auth.items():
            with self.subTest(urls=urls):
                response = self.auth_client.get(urls)
                self.assertEqual(response.status_code, status)

        for urls, status in urls_names_not_auth.items():
            with self.subTest(urls=urls):
                response = self.guest_client.get(urls)
                self.assertEqual(response.status_code, status)

    def test_urls_uses_correct_templates(self):
        """Проверка на корректность используемых html-шаблонов"""
        templates_urls_names = {
            '/': 'films/index.html',
            '/favorite/': 'films/films_favorites.html',
            '/watched/': 'films/films_watched.html',
            '/deferred/': 'films/deferred_films.html',
            # указываемый данный id так как фильм берется из внешнего API
            '/film/685246/': 'films/film.html',
            '/recommendation/': 'films/recommended_films.html',
            '/search/': 'films/search_result.html',
            '/error/': 'films/error_api.html',
        }

        for address, template in templates_urls_names.items():
            with self.subTest(address=address):
                response = self.auth_client.get(address)
                self.assertTemplateUsed(response, template)
