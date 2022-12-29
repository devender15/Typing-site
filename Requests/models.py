from django.db import models

# Create your models here.

class Request(models.Model):
    text = models.TextField(null=True)
    teacher_name = models.CharField(max_length=100, blank=True, null=True)
    tag = models.CharField(max_length=10, null=True, default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tag + " " + self.teacher_name
