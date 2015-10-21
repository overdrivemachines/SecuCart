from django.db import models
from django.contrib.auth.models import User

class Item(models.Model):
	name = models.CharField(max_length=100, default='TOTALLY AN ITEM GUYS')
	description = models.CharField(max_length=255, default='')
	quantity = models.IntegerField(default=0)
