from django.db import models
# from base.models import Employee
# Create your models here.
class Department(models.Model):
    DepID = models.IntegerField(primary_key=True)
    DepName = models.CharField(max_length=255)
    EmpID = models.ForeignKey('base.Employee',on_delete=models.SET_NULL,null=True)