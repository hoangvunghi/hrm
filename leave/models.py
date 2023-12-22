from django.db import models
from base.models import Employee
from leave_type.models import LeaveType
# Create your models here.
class Leave(models.Model):
    LeaveID = models.AutoField(primary_key=True)
    EmpID = models.ForeignKey(Employee, on_delete=models.CASCADE)
    LeaveStartDate = models.DateTimeField()
    LeaveEndDate = models.DateTimeField()
    LeaveTypeID = models.ForeignKey(LeaveType, on_delete=models.CASCADE)
    Reason = models.CharField(max_length=500)
    LeaveStatus = models.CharField(max_length=255)