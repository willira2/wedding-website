from django.db import models
import datetime

from django.utils import timezone


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

class Party(models.Model):
	name = models.CharField(max_length=50)

	def __str__(self):
		return self.name
		

class Invitation(models.Model):
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	status = models.IntegerField(default=0)
	party = models.ForeignKey(Party, on_delete=models.CASCADE)

	def __str__(self):
		return u'%s %s' % (self.first_name, self.last_name)
		