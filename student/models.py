from django.db import models

class Student(models.Model):

    # user_id = models.IntegerField()
    # username = models.CharField(max_length=100)
    # phn_no = models.IntegerField()
    name = models.CharField(max_length=30,default='')
    email = models.CharField(max_length=100,default='')
    password = models.CharField(max_length=100,default='')
    institute = models.CharField(max_length=100, null=True)
    age = models.IntegerField(default=10)
    standard = models.IntegerField(default=5)
    speed = models.IntegerField(default=0)

class Analysis(models.Model):
    ana_id = models.IntegerField(null=True)
    status = models.IntegerField(default=0)
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
    hint = models.IntegerField(null=True)
    wasted = models.IntegerField(null=True)
    test_id = models.IntegerField()

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
    kcids = models.CharField(max_length=1000 , null=False)

class Motivation(models.Model):
    mot_id = models.IntegerField()
    mot_quote = models.CharField(max_length=1000 , null=False)
    mots_id = models.IntegerField()

class Kc(models.Model):
    kc_id = models.IntegerField(primary_key=True)
    priority = models.IntegerField()

class Kc_ana(models.Model):
    stu_id = models.IntegerField()
    kc_id = models.IntegerField()
    status = models.IntegerField()
    p_list = models.CharField(max_length=1000 , null=False)

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
    step1 = models.IntegerField(default=-1)
    step2 = models.IntegerField(default=-1)
    step3 = models.IntegerField(default=-1)
    solution = models.CharField(max_length=1000 , null=False)
    best_time = models.IntegerField()
    avg_time = models.IntegerField()
    que_no = models.IntegerField()
    attempt = models.IntegerField()
    test_id = models.IntegerField()
    speed = models.IntegerField(default=0)
    kcid = models.CharField(max_length=1000 , default="1")

class Imaged(models.Model):
    img_id = models.IntegerField(primary_key=True)
    sub_id = models.IntegerField(default=0)
    top_id = models.IntegerField(default=0)
    que_id = models.IntegerField(default=0)
    location = models.CharField(max_length=1000 , null=False)
    mot_id = models.IntegerField(default=0)

class Forum(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100 , null=False)
    desc =  models.CharField(max_length=1000 , null=False)
    # user_id = models.IntegerField(null=True)
    username =  models.CharField(max_length=100 , null=False)
    email =  models.CharField(max_length=100,default='')
    date = models.CharField(max_length = 20)

class Forum_reply(models.Model):
    id = models.AutoField(primary_key=True)
    forum_id = models.IntegerField()
    # reply_id = models.IntegerField()
    desc = models.CharField(max_length=1000 , null=False)
    # user_id = models.IntegerField(null=True)
    username =  models.CharField(max_length=100 , null=False)
    email =  models.CharField(max_length=100,default='')
    date = models.CharField(max_length = 20)

class Subtopic(models.Model):
    subtop_id = models.IntegerField(primary_key=True)
    subtop_name = models.CharField(max_length=1000 , null=False)
    top_id = models.IntegerField()
    kcid = models.CharField(max_length=1000 , null=False)

class St_ana(models.Model):
    stana_id = models.IntegerField(primary_key=True)
    complete_per = models.IntegerField(default=0)
    user_id = models.IntegerField(null=True)
    topic_id = models.IntegerField(null=True)
    time = models.IntegerField(null=True)