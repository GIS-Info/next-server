from django.db import models

class Person(models.Model):
    person_name_cn = models.CharField(max_length=255)
    person_name_en = models.CharField(max_length=255)
    url = models.URLField()
    physical_geography = models.BooleanField(default=False)
    human_geography = models.BooleanField(default=False)
    urban_planning = models.BooleanField(default=False)
    gis = models.BooleanField(default=False)
    rs = models.BooleanField(default=False)
    gnss = models.BooleanField(default=False)
    research_interests = models.TextField(null=True, blank=True)
    university = models.CharField(max_length=255)
    people_id = models.AutoField(primary_key=True)
    transportation = models.BooleanField(default=False)
    class Meta:
        db_table = 'new_people'  # Explicitly set the table name
        managed = True
    