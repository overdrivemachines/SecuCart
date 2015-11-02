from django.db import models
from django.contrib.auth.models import User

class Item(models.Model):
	name = models.CharField(max_length=100, default='TOTALLY AN ITEM GUYS')
	description = models.CharField(max_length=255, default='')
	quantity = models.IntegerField(default=0)

class Cart(models.Model):
	user = models.CharField(max_length=100, default='Default_user')
	items = models.ManyToManyField("Item")

	@property
	def item_list(self):
	    return list(self.items.all())
	