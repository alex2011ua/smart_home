from django.db import models

class Words(models.Model):
    english = models.CharField(max_length=128)
    russian = models.CharField(max_length=128)

