from django.db import models

class Student(models.Model):
    user_id = models.IntegerField()
    username = models.CharField(max_length=100 , null=False)


class Analysis(models.Model):
    user_id = models.IntegerField()
    sub_id = models.IntegerField()
    topic_id = models.IntegerField()
    mot_id = models.IntegerField()
    confidence = models.IntegerField()
    confidence_s = models.IntegerField()
    que_id = models.IntegerField()
    correct = models.IntegerField()
    attempt = models.IntegerField()
    time = models.IntegerField()
    last_time = models.IntegerField()
    best_time = models.IntegerField()
    effort = models.IntegerField()

class Subject(models.Model):
    sub_id = models.IntegerField()
    sub_name = models.CharField(max_length=1000 , null=False)
    mots_id = models.IntegerField()
    confidence_s = models.IntegerField()

class topic(models.Model):
    top_id = models.IntegerField()
    top_name = models.CharField(max_length=1000 , null=False)
    level = models.IntegerField()

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
