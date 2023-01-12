from django.db import models
import string, random


def generate_unique_code():

    length = 6

    while 1:
        code = "".join(random.choices(string.ascii_uppercase, k=length))
        if(Room.objects.filter(code=code).count() == 0):
            break
    
    return code

class Room(models.Model):
    code = models.CharField(max_length=8, default=generate_unique_code, unique=True)
    host = models.CharField(max_length=100, unique=False)
    exam = models.CharField(max_length=100, unique=False, blank=True)
    test_name = models.CharField(max_length=100, unique=False, blank=True)
    test_id = models.IntegerField(unique=False, blank=True, null=True)
    time = models.IntegerField(default=60)
    paragraph = models.CharField(max_length=20, blank=True)
    criteria = models.TextField()
    participants = models.IntegerField(default=1, null=True)
    isExpired = models.BooleanField(default=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.host + " " + str(self.created_at)
