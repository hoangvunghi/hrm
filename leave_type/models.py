from django.db import models

# Create your models here.
class LeaveType(models.Model):
    LeaveTypeID = models.AutoField(primary_key=True)
    LeaveTypeName = models.CharField(max_length=255)
    Subsidize=models.FloatField()