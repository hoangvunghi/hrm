from django.db import models
from base.models import Employee
# Create your models here.
from django.utils import timezone

class TimeSheet(models.Model):
    TimeID = models.AutoField(primary_key=True)
    TimeIn = models.DateTimeField(null=True, blank=True)
    TimeOut = models.DateTimeField(null=True, blank=True)
    EmpID = models.ForeignKey(Employee, on_delete=models.CASCADE)    
    data_dict = models.JSONField(default=dict)
    