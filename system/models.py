from django.db import models


class ModelManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(isValid=1)


class Role(models.Model):

    roleName = models.CharField(max_length=20, db_column='role_name')
    roleRemark = models.CharField(max_length=120, db_column='role_remark')
    isValid = models.IntegerField(db_column='is_valid')
    createDate = models.DateTimeField(db_column='create_date')
    updateDate = models.DateTimeField(max_length=20, db_column='update_date')

    objects = ModelManager()

    class Meta:
        db_table = 't_role'


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

    roles = models.ManyToManyField(Role, through="UserRole", through_fields=('user', 'role'))

    objects = ModelManager()

    class Meta:
        db_table = 't_user'


# 用户-角色中间表
class UserRole(models.Model):
    user = models.ForeignKey(User, db_column='user_id',
                             db_constraint=False, on_delete=models.DO_NOTHING)

    role = models.ForeignKey(Role, db_column='role_id',
                             db_constraint=False, on_delete=models.DO_NOTHING)

    isValid = models.IntegerField(db_column='is_valid')
    createDate = models.DateTimeField(db_column='create_date')
    updateDate = models.DateTimeField(max_length=20, db_column='update_date')

    objects = ModelManager()

    class Meta:
        db_table = 't_user_role'
