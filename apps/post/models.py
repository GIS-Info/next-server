from django.db import models
from nextServer import settings

# Create your models here.
class GISource(models.Model):
    """
    Each post contains the information: post_id, job, country, term, tag, end_month, query_string
    """
    event_id = models.AutoField(primary_key = True)
    university_fk = models.IntegerField()
    required_degree = models.IntegerField()
    contact1 = models.CharField(max_length=20)
    email1 = models.CharField(max_length=20)
    contact2 = models.CharField(max_length=20)
    email2 = models.CharField(max_length=20)
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

    class Meta:
        managed = False
        db_table = 'GISource'






