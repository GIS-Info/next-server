from django.db import models
from nextServer import settings

# Create your models here.
class GISource(models.Model):
    """
    Each post contains the information: post_id, job, country, term, tag, end_month, query_string
    """
    """
    改用新的表结构
    """
    event_id = models.AutoField(primary_key = True)
    university_cn = models.CharField(max_length=100)
    university_en = models.CharField(max_length=100)
    country_cn = models.CharField(max_length=100)
    country_en = models.CharField(max_length=100)
    job_cn = models.CharField(max_length=100)
    job_en = models.CharField(max_length=100)
    description = models.CharField(max_length=5000)
    title_cn = models.CharField(max_length=400)
    title_en = models.CharField(max_length=400)
    label_physical_geo = models.SmallIntegerField()
    label_human_geo = models.SmallIntegerField()
    label_urban = models.SmallIntegerField()
    label_gis = models.SmallIntegerField()
    label_rs = models.SmallIntegerField()
    label_gnss = models.SmallIntegerField()
    date = models.DateField()
    is_public = models.SmallIntegerField()
    is_deleted = models.SmallIntegerField()

    '''
    event_id = models.AutoField(primary_key = True)
    university_fk = models.IntegerField()
    required_degree = models.IntegerField()
    contact1 = models.CharField(max_length=40)
    email1 = models.CharField(max_length=40)
    contact2 = models.CharField(max_length=40)
    email2 = models.CharField(max_length=40)
    url = models.CharField(max_length=255)
    post_date = models.DateField()
    close_date = models.DateField()
    start_date = models.DateField()
    job_fk = models.IntegerField()
    has_close_date = models.SmallIntegerField(max_length=1)
    number_of_vacancy = models.IntegerField()
    vacancy_name = models.CharField(max_length=20)
    vacancy_rank = models.CharField(max_length=20)
    label = models.TextField()
    still_open = models.SmallIntegerField()
    verified = models.SmallIntegerField()
    provider = models.CharField(max_length=20)
    provider_email = models.CharField(max_length=255)
    country = models.IntegerField()
    job_title = models.CharField(max_length=55)
    queryString = models.CharField(max_length=55)
    detail = models.TextField()
    '''

    class Meta:
        managed = False
        db_table = 'GISource'

'''
class Countries(models.Model):
    Country_ID = models.AutoField(primary_key = True)
    Country_Name_CN = models.CharField(max_length=20)
    Country_Name_EN = models.CharField(max_length=20)
    Continent_FK = models.CharField(max_length=20)
    Continent = models.CharField(max_length=20)
    class Meta:
        managed = False
        db_table = 'Countries'
'''

