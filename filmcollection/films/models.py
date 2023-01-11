from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Film(models.Model):
    film_id = models.IntegerField()
    name_ru = models.CharField(max_length=128, null=True)
    name_en = models.CharField(max_length=128, null=True)
    name_original = models.CharField(max_length=128, null=True)
    year = models.SmallIntegerField()
    description = models.CharField(max_length=1024, null=True)
    film_length = models.SmallIntegerField(null=True)
    rating = models.CharField(max_length=16, null=True)
    image = models.CharField(max_length=1024, null=True)


class WatchedFilm(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watched_film')
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='watched_film')
    rating = models.SmallIntegerField()
    pub_date = models.DateTimeField(auto_now_add=True)


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite')
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='favorite')
    pub_date = models.DateTimeField(auto_now_add=True)


class Deferred(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='deferred')
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='deferred')
    pub_date = models.DateTimeField(auto_now_add=True)
