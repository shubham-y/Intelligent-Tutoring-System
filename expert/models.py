from django.db import models

class Expert(models.Model):
    name = models.CharField(max_length=30,default='')
    email = models.CharField(max_length=100,default='')
    password = models.CharField(max_length=100,default='')
    institute = models.CharField(max_length=100, null=True)
    age = models.IntegerField(default=10)
