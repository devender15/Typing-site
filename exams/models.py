from django.db import models

# Create your models here.

class Exams(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    attempts = models.IntegerField(null=True, blank=True, default=0)
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

    def __str__(self):
        return self.name