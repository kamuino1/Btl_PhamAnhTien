from __future__ import unicode_literals
from django.db import models

# Create your models here.
class comment(models.Model):
    username = models.CharField(max_length=50)
    date_added = models.DateTimeField(auto_now_add=True)
    product_id = models.CharField(max_length=10)
    content = models.CharField(max_length=255)  
    ### It will help to print the values.
    def __str__(self):
        return '%s %s %s %s ' % (self.username, self.product_id,
            self.content, self.date_added)
