from django.db import models
from base.models import Employee
# Create your models here.
class SalaryHistory(models.Model):
    EmpID=models.ForeignKey(Employee,on_delete=models.CASCADE)
    SalFrom=models.DateField()
    SalEnd=models.DateField()
    SalAmount=models.FloatField()
    class Meta:
        unique_together=(('EmpID',"SalFrom"),)
