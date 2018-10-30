from django.db import models

# Create your models here.
class profile(models.Model):
	title=models.CharField(max_length=100)
	image=models.FileField()

class comments(models.Model):
	user=models.CharField(max_length=100)
	title=models.CharField(max_length=100)
	comment=models.CharField(max_length=100)

class login1(models.Model):
	username=models.CharField(primary_key = True, max_length=100)
	password=models.CharField(max_length=100)