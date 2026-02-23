from django.db import models


# Create your models here.
# 因为现有数据没有严格遵守关联关系，所以无法建立表关联，暂时通过 sql join 来关联
class School(models.Model):
  Universities_id = models.AutoField(primary_key = True)
  University_Name_CN = models.CharField(max_length=255,blank=True,null=True)
  University_Name_EN = models.CharField(max_length=255,blank=True,null=True)
  University_Name_Local = models.CharField(max_length=255,blank=True,null=True)
  City = models.CharField(max_length=255,blank=True,null=True)
  URL = models.CharField(max_length=255,blank=True,null=True)
  University_Abbr = models.CharField(max_length=255,blank=True,null=True)
  University_Other_Name = models.CharField(max_length=255,blank=True,null=True)
  Description_CN = models.CharField(max_length=5000,blank=True,null=True)
  Description_EN = models.CharField(max_length=5000,blank=True,null=True)
  Unit_CN = models.CharField(max_length=255,blank=True,null=True)
  Unit_EN = models.CharField(max_length=255,blank=True,null=True)
  Lon = models.DecimalField(max_digits=6, decimal_places=2)
  Lat = models.DecimalField(max_digits=6, decimal_places=2)
  class Meta:
    managed = False
    db_table = 'new_Universities'
