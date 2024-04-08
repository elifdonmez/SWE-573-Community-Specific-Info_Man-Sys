from django.db import models


class User(models.Model):

    class Meta:
        db_table = 'users'

    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)


class Community(models.Model):

    class Meta:
        db_table = 'communities'

    name = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=600)
    privacy = models.CharField(max_length=200)


class UserCommunity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_communities'
