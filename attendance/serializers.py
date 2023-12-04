from base.models import Attendance
from rest_framework import serializers


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        # fields = ["check_out_time","employee_id"]
        fields="__all__"
        
        
# class Attendance(models.Model):
#     attendance_id = models.AutoField(primary_key=True)
#     employee_id = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
#     attendance_date = models.DateField(auto_now=True)
#     check_in_time = models.DateTimeField(auto_now=True)
#     check_out_time = models.DateTimeField()
    
#     STATUS_CHOICES = [
#         ('ontime', 'OnTime'),
#         ('late', 'Late'),
#         ('absent', 'Absent'),
#     ]
#     status = models.CharField(
#         max_length=10,
#         choices=STATUS_CHOICES,
#         default='ontime',
#     )
