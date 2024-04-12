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
    rules = models.CharField(max_length=10000, default="No Rules")
    creator = models.CharField(max_length=200)


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
    header = models.CharField(max_length=500)
    description = models.CharField(max_length=1000)
    number_of_upvotes = models.IntegerField()
    number_of_downvotes = models.IntegerField()
    number_of_smiles = models.IntegerField()
    number_of_hearts = models.IntegerField()
    number_of_sadfaces = models.IntegerField()

class Comments(models.Model):

    class Meta:
        db_table = 'comments'

    commenter_email =  models.CharField(max_length=600)
    comment_content =  models.CharField(max_length=600)
    post_id =  models.CharField(max_length=600)



