from django.db import models

# Create your models here.


class Transaction(models.Model):
    title = models.CharField(max_length=70, blank=False, default='')
    transaction_url = models.CharField(max_length=200, blank=False, default='')
    image_path = models.CharField(max_length=150, blank=True, null=True)
    description = models.CharField(max_length=200, blank=False, default='')
    published = models.BooleanField(default=False)
