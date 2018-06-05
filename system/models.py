from django.db import models


class UserManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(isValid=1)


# Create your models here.
class User(models.Model):

    userName = models.CharField(max_length=20, db_column='user_name')
    password = models.CharField(max_length=20, db_column='password')
    trueName = models.CharField(max_length=20, db_column='true_name')
    email = models.EmailField(max_length=20, db_column='email')
    phone = models.CharField(max_length=20, db_column='phone')
    isValid = models.IntegerField(db_column='is_valid')
    createDate = models.DateTimeField(db_column='create_date')
    updateDate = models.DateTimeField(max_length=20, db_column='update_date')

    objects = UserManager()

    class Meta:
        db_table = 't_user'
