from django.db import models

class Student(models.Model):
    user_id = models.IntegerField()
    username = models.CharField(max_length=100 , null=False)
    phn_no = models.IntegerField()
    email = models.CharField(max_length=100 , null=False)
    inst = models.CharField(max_length=100 , null=False)
    age = models.IntegerField()
    standard = models.IntegerField()



class Analysis(models.Model):
    user_id = models.IntegerField(null=True)
    sub_id = models.IntegerField(null=True)
    topic_id = models.IntegerField(null=True)
    mot_id = models.IntegerField(null=True)
    confidence = models.IntegerField(null=True)
    confidence_s = models.IntegerField(null=True)
    que_id = models.IntegerField(null=True)
    correct = models.IntegerField(null=True)
    attempt = models.IntegerField(null=True)
    time = models.IntegerField(null=True)
    last_time = models.IntegerField(null=True)
    best_time = models.IntegerField(null=True)
    effort = models.IntegerField(null=True)

class Subject(models.Model):
    sub_id = models.IntegerField()
    sub_name = models.CharField(max_length=1000 , null=False)
    mots_id = models.IntegerField()
    confidence_s = models.IntegerField()

class topic(models.Model):
    top_id = models.IntegerField()
    top_name = models.CharField(max_length=1000 , null=False)
    level = models.IntegerField()
    sub_id = models.IntegerField()

class Motivation(models.Model):
    mot_id = models.IntegerField()
    mot_quote = models.CharField(max_length=1000 , null=False)
    mots_id = models.IntegerField()

class Quetions(models.Model):
    que_id = models.IntegerField()
    question = models.CharField(max_length=1000 , null=False)
    opt_1 = models.CharField(max_length=1000 , null=False)
    opt_2 = models.CharField(max_length=1000 , null=False)
    opt_3 = models.CharField(max_length=1000 , null=False)
    opt_4 = models.CharField(max_length=1000 , null=False)
    sub_id = models.IntegerField()
    top_id = models.IntegerField()
    hint = models.CharField(max_length=1000 , null=False)
    level = models.IntegerField()
    ans = models.IntegerField()
