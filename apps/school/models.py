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


class NewUniversity(models.Model):
    Universities_id = models.AutoField(primary_key=True)
    University_Name_CN = models.CharField(max_length=255)
    University_Name_EN = models.CharField(max_length=255)
    University_Name_Local = models.CharField(max_length=255)
    City = models.CharField(max_length=255)
    URL = models.CharField(max_length=512)
    University_Abbr = models.CharField(max_length=255)
    University_Other_Name = models.CharField(max_length=255)
    Description_CN = models.TextField()
    Description_EN = models.TextField()
    Unit_CN = models.CharField(max_length=255)
    Unit_EN = models.CharField(max_length=255)
    Lon = models.FloatField()
    Lat = models.FloatField()

    class Meta:
        managed = False
        db_table = 'new_Universities'

    def __str__(self):
        return self.University_Name_EN


class Cities(models.Model):
    City_id = models.AutoField(primary_key=True)
    City_Name_CN = models.CharField(max_length=255)
    City_Name_EN = models.CharField(max_length=255)
    Country = models.CharField(max_length=255)
    Lat = models.CharField(max_length=255)
    Lon = models.CharField(max_length=255)
    City_Name_Other = models.CharField(max_length=255)
    f7 = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'new_city'

class Countries (models.Model):
    Country_id = models.AutoField(primary_key=True)
    f4 = models.CharField(max_length=255)
    Continent = models.CharField(max_length=255)
    Country_Name_CN = models.CharField(max_length=255)
    Country_Name_EN = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'new_country'
