from django.db import models
from department.models import Department
# Create your models here.
class Job(models.Model):
    JobID = models.AutoField(primary_key=True)
    JobName = models.CharField(max_length=255)
    JobChangeHour=models.FloatField()
    DepID=models.ForeignKey(Department,on_delete=models.CASCADE)
