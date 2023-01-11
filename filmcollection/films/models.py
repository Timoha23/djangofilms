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


class UserRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    rating = models.SmallIntegerField()
    pub_date = models.DateTimeField(auto_now_add=True)
