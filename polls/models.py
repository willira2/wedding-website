from django.db import models
import datetime
from .choices import *

from django.utils import timezone

class Party(models.Model):
	name = models.CharField(max_length=50)
	invite_code = models.CharField(null=True,max_length=15)

	def __str__(self):
		return self.name

class Invitation(models.Model):
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=None)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    party = models.ForeignKey(Party, on_delete=models.CASCADE)

    def __str__(self):
        return u'%s %s' % (self.first_name, self.last_name)


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

