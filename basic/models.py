from django.db import models


class ModelManager(models.Manager):

    def get_queryset(self):
        return super(ModelManager, self).get_queryset().filter(isValid=1)


# Create your models here.
class DataDic(models.Model):
    dataDicName = models.CharField(max_length=20, db_column='data_dic_name')
    dataDicValue = models.CharField(max_length=20, db_column='data_dic_value')
    isValid = models.IntegerField(db_column='is_valid')
    createDate = models.DateTimeField(db_column='create_date')
    updateDate = models.DateTimeField(max_length=20, db_column='update_date')
    objects = ModelManager()

    class Meta:
        db_table = 't_datadic'
