from django.db import models


class User(models.Model):

    class Meta:
        db_table = 'users'

    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)