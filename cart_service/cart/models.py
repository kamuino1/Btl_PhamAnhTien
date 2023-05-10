from django.db import models
from rest_framework import serializers

class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50)
    date_added = models.DateTimeField(auto_now_add=True)
    product_id = models.CharField(max_length=10)
    quantity = models.IntegerField(default=1)
    def __str__(self):
        return '%s %s %s %s %s' % (self.id, self.username, self.date_added, self.product_id, self.quantity)