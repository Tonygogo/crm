from django.db import models


class SaleChanceManager(models.Manager):

    def get_queryset(self):
        return super(SaleChanceManager, self).get_queryset().filter(isValid=1)


# Create your models here.
class SaleChance(models.Model):

    chanceSource = models.CharField(max_length=300, db_column='chance_source')
    customerId = models.IntegerField(db_column='customer_id')
    customerName = models.CharField(max_length=100, db_column='customer_name')
    # 成功几率
    cgjl = models.IntegerField(db_column='cgjl')
    # 概要
    overview = models.CharField(max_length=300, db_column='overview')
    # 联系人
    linkMan = models.CharField(max_length=20, db_column='link_man')
    # 联系电话
    linkPhone = models.CharField(max_length=20, db_column='link_phone')
    # 描述
    description = models.CharField(max_length=1000, db_column='description')
    # 创建人
    createMan = models.CharField(max_length=20, db_column='create_man')
    # 分配给谁
    assignMan = models.CharField(max_length=20, db_column='assign_man')
    # 分配时间
    assignTime = models.DateTimeField(db_column='assign_time', auto_now_add=True)
    # 状态：1-如果有分配就是已分配状态，0-未分配
    state = models.CharField(max_length=20, db_column='state')
    # 开发状态：0=未开发 1=开发中 2=开完完成 3=开发失败
    devResult = models.CharField(max_length=20, db_column='dev_result')

    isValid = models.IntegerField(db_column='is_valid')
    createDate = models.DateTimeField(db_column='create_date')
    updateDate = models.DateTimeField(max_length=20, db_column='update_date')

    objects = SaleChanceManager()

    class Meta:
        db_table = 't_sale_chance'
