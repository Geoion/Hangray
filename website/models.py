from django.db import models
from django.contrib.auth.models import User


class UserInfo(models.Model):
    avatar = models.FileField(upload_to='avatar/%Y/%m/%d', null=True)
    account = models.OneToOneField(User)
    city = models.CharField(max_length=20, null=True)
    short_introduce = models.CharField(max_length=100, null=True)
    introduce = models.CharField(max_length=500, null=True)
    industry = models.CharField(max_length=20, null=True)
    like_number = models.IntegerField()
    question_number = models.IntegerField()
    mark_number = models.IntegerField()
    register_time = models.DateTimeField(auto_created=True)
    phone_number = models.IntegerField(max_length=15)
    sex = models.CharField(max_length=2)


class Question(models.Model):
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=5000)
    time = models.DateTimeField(auto_created=True, auto_now=True)
    topic = models.CharField(max_length=10)
    account = models.ForeignKey(User)


class Answer(models.Model):
    content = models.CharField(max_length=500)
    time = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User)
    question = models.ForeignKey(Question)


class Comment(models.Model):
    content = models.CharField(max_length=100)
    time = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User)
    answer = models.ForeignKey(Answer)


class Follow(models.Model):
    follower = models.ForeignKey(User, null=True, related_name='follower')
    follow_by = models.ForeignKey(User, null=True, related_name='follower_by')
    time = models.DateTimeField(auto_now=True)


class Event(models.Model):
    time = models.DateTimeField(auto_now=True)
    account = models.ForeignKey(User)
    question = models.ForeignKey(Question, null=True)
    answer = models.ForeignKey(Answer, null=True)