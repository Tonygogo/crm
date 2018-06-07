from django.db import models


class CustomerManager(models.Manager):

    def get_queryset(self):
        return super(CustomerManager, self).get_queryset().filter(isValid=1)

# Create your models here.


class Customer(models.Model):

    khno = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=20)
    area = models.CharField(max_length=20)
    cus_manager = models.CharField(max_length=30)
    level = models.IntegerField()
    myd = models.CharField(max_length=30)
    xyd = models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    post_code = models.CharField(max_length=10)
    phone = models.CharField(max_length=18)
    fax = models.CharField(max_length=20)
    web_site = models.CharField(max_length=50)
    yyzzzch = models.CharField(max_length=50)
    fr = models.CharField(max_length=20)
    zczj = models.CharField(max_length=20)
    nyye = models.CharField(max_length=20)
    khyh = models.CharField(max_length=20)
    khzh = models.CharField(max_length=20)
    dsdjh = models.CharField(max_length=20)
    gsdjh = models.CharField(max_length=20)
    state = models.IntegerField()
    isValid = models.IntegerField(db_column='is_valid')
    createDate = models.DateTimeField(db_column='create_date', auto_now_add=True)
    updateDate = models.DateTimeField(db_column='update_date', auto_now_add=True)

    objects = CustomerManager()

    class Meta:
        db_table = 't_customer'
