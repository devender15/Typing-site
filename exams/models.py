from django.db import models
from UserAuthentication.models import User

# Create your models here.

class Exams(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    attempts = models.IntegerField(null=True, blank=True, default=0)
    ratings = models.JSONField(null=True, blank=True) # it is an array of ratings
    rating = models.FloatField(null=True, blank=True, default=0)
    user_rated = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    added_on = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

class Tests(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    exam = models.ForeignKey(Exams, on_delete=models.CASCADE)
    language = models.CharField(max_length=50, null=True, blank=True)
    attempts = models.IntegerField(null=True, blank=True, default=0)
    ratings = models.IntegerField(null=True, blank=True, default=0)
    teacher = models.CharField(max_length=100, null=True, blank=True)
    institute = models.CharField(max_length=100, null=True, blank=True)
    live = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return self.name
