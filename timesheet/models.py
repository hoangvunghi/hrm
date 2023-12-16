from django.db import models
from base.models import Employee
# Create your models here.
class TimeSheet(models.Model):
    TimeID = models.IntegerField(primary_key=True)
    TimeIn = models.DateTimeField()
    TimeOut = models.DateTimeField()
    EmpID = models.ForeignKey(Employee, on_delete=models.CASCADE)