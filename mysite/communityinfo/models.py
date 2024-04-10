from django.db import models


class RegisteredUser(models.Model):

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

    class Meta:
        db_table = 'user_communities'

    username = models.CharField(max_length=600)
    community_name = models.CharField(max_length=600)


class UserFollower(models.Model):

    class Meta:
        db_table = 'user_followers'

    username = models.CharField(max_length=600)
    follower_username = models.CharField(max_length=600)


class Posts(models.Model):

    class Meta:
        db_table = 'posts'

    community_name =  models.CharField(max_length=600)
    submitter_name =  models.CharField(max_length=600)


class Comments(models.Model):

    class Meta:
        db_table = 'comments'

    commenter_email =  models.CharField(max_length=600)
    comment_content =  models.CharField(max_length=600)
    post_id =  models.CharField(max_length=600)
