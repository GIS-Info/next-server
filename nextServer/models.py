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

class University(models.Model):
    university_name_cn = models.CharField(max_length=255)
    university_name_en = models.CharField(max_length=255)
    university_name_local = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    url = models.URLField()
    university_abbr = models.CharField(max_length=255)
    university_other_name = models.CharField(max_length=255)
    description_cn = models.TextField()
    description_en = models.TextField()
    unit_cn = models.CharField(max_length=255)
    unit_en = models.CharField(max_length=255)
    lon = models.FloatField()
    lat = models.FloatField()
    universities_id = models.IntegerField(primary_key=True)
    physical_geography = models.BooleanField()
    human_geography = models.BooleanField()
    urban_planning = models.BooleanField()
    gis = models.BooleanField()
    rs = models.BooleanField()
    gnss = models.BooleanField()
    transportation = models.BooleanField()

    class Meta:
        db_table = 'new_Universities'  # Ensure this matches your actual table name
        managed = True
    