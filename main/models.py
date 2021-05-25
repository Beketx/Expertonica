from django.db import models

class HtmlPage(models.Model):
    text = models.TextField()

class ParseModel(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    url = models.CharField(max_length=255, null=True, blank=True)

