from django.db import models

from django.contrib.postgres.fields import JSONField
# Create your models here.

class orders(models.Model):
    shipid = models.AutoField(primary_key=True, )
    status = models.CharField(blank = False, max_length = 256, default="InWareHouse")
    userid = models.IntegerField(blank=False)
    addressx = models.IntegerField(blank=False)
    addressy = models.IntegerField(blank=False)
    upsid = models.CharField(blank = True, max_length = 256)

class wareHouse(models.Model):
    productid = models.AutoField(primary_key=True, )
    productname = models.CharField(blank=False, max_length=256)
    description = models.CharField(blank=False, max_length=256)
    count = models.IntegerField(blank=False)
    def __str__(self):
        return str(self.productname)

class truck(models.Model):
    shipid = models.IntegerField(blank=True,)
    truckid = models.IntegerField(blank=True, )

class upsack(models.Model):
    ack = models.IntegerField(blank=False)

class worldack(models.Model):
    ack = models.IntegerField(blank = False)

class upsseq(models.Model):
    seqnum = models.IntegerField(blank = False)
    message = JSONField()
    time = models.DateTimeField(auto_now = True)

class worldseq(models.Model):
    seqnum = models.IntegerField(blank = False)
    message = JSONField()
    time = models.DateTimeField(auto_now = True)

class topack(models.Model):
    packageid = models.IntegerField(blank = False)
    message = JSONField()

class placed(models.Model):
    packageid = models.IntegerField(blank=False)
    message = JSONField()
