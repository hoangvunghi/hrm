from django.db import models
from department.models import Department
# Create your models here.
class Job(models.Model):
    JobID = models.AutoField(primary_key=True)
    JobName = models.CharField(max_length=255)
    DepID=models.ForeignKey(Department,on_delete=models.SET_NULL,null=True,blank=True)
    Descriptions=models.CharField(max_length=1000,null=True)
