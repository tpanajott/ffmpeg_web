from django.db import models
import os

# Create your models here.

class Preset(models.Model):
    name = models.CharField(max_length=200, default="", unique=True)
    arguments = models.TextField()

class ConvertJob(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    source = models.CharField(max_length=1000)
    destination = models.CharField(max_length=1000)
    preset = models.ForeignKey(Preset, on_delete=models.CASCADE)
    custom_arguments = models.TextField()
    log = models.TextField()
    status = models.CharField(max_length=50)
    percentage = models.FloatField(default=0)
    error_text = models.TextField()
    time_left = models.CharField(max_length=50)
    speed = models.FloatField(default=0)
    total_length_seconds = models.IntegerField(default=0)

    def source_file_name(self):
        return os.path.basename(self.source)