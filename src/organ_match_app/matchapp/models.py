from django.db import models
from django.contrib.auth.models import User

class Doctors(models.Model):
    name = models.CharField(max_length=20)
    specialty = models.CharField(max_length=20)
    experience = models.IntegerField(blank = True, null=True)

class Person(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField(auto_now=False, auto_now_add=False, null=False)
    blood_type = models.CharField(max_length=4)
    doctor_id = models.IntegerField(blank=True, null=True) 

    def __str__(self):
        return f'{self.user.username} Profile'

class Needs(models.Model):
    user_id = models.IntegerField()
    organ = models.CharField(max_length=20)
    date_by = models.DateField(auto_now=False, auto_now_add=False, null=False)
    
    class Meta:
        unique_together = (("user_id", "organ"),)

class Available(models.Model):
    organ = models.CharField(max_length=20)
    user_id = models.IntegerField()

    class Meta:
        unique_together = (("user_id", "organ"),)