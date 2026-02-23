from django.db import models

# Create your models here.
class GISource(models.Model):
    """
    Each post contains the information: post_id, job, country, term, tag, end_month, query_string
    """
    """
    改用新的表结构
    """
    event_id = models.AutoField(primary_key = True)
    university_cn = models.CharField(max_length=100,blank=True,null=True)
    university_en = models.CharField(max_length=100,blank=True,null=True)
    country_cn = models.CharField(max_length=100,blank=True,null=True)
    country_en = models.CharField(max_length=100,blank=True,null=True)
    job_cn = models.CharField(max_length=100,blank=True,null=True)
    job_en = models.CharField(max_length=100,blank=True,null=True)
    description = models.CharField(max_length=5000,blank=True,null=True)
    title_cn = models.CharField(max_length=400,blank=True,null=True)
    title_en = models.CharField(max_length=400,blank=True,null=True)
    label_physical_geo = models.SmallIntegerField(blank=True,null=True)
    label_human_geo = models.SmallIntegerField(blank=True,null=True)
    label_urban = models.SmallIntegerField(blank=True,null=True)
    label_gis = models.SmallIntegerField(blank=True,null=True)
    label_rs = models.SmallIntegerField(blank=True,null=True)
    label_gnss = models.SmallIntegerField(blank=True,null=True)
    date = models.DateField(blank=True,null=True)
    is_public = models.SmallIntegerField()
    is_deleted = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'GISource'
