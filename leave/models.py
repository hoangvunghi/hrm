from django.db import models
from base.models import Employee
from leave_type.models import LeaveType
# Create your models here.
class LeaveRequest(models.Model):
    LeaveRequestID = models.AutoField(primary_key=True)
    EmpID = models.ForeignKey(Employee, on_delete=models.CASCADE)
    LeaveStartDate = models.DateField()
    LeaveEndDate = models.DateField()
    LeaveTypeID = models.ForeignKey(LeaveType, on_delete=models.CASCADE)
    Reason = models.CharField(max_length=500)
    STATUS_CHOICES = [
        ('Chờ xác nhận', 'Chờ xác nhận'),
        ('Chờ phê duyệt', 'Chờ phê duyệt'),
        ('Đã phê duyệt', 'Đã phê duyệt'),
        ('Đã từ chối', 'Đã từ chối'),
    ]

    LeaveStatus = models.CharField(
        max_length=255,
        choices=STATUS_CHOICES,
        default='Chờ xác nhận',
    )
    Duration=models.IntegerField()
    
    def save(self, *args, **kwargs):
        if self.LeaveStartDate and self.LeaveEndDate:
            self.Duration = (self.LeaveEndDate - self.LeaveStartDate).days + 1
        self.Duration = int(self.Duration)
        super(LeaveRequest, self).save(*args, **kwargs)
        
