from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from datetime import datetime

class Positions(models.Model):
    position_id = models.AutoField(primary_key=True)
    position_name = models.CharField(max_length=200)

class UserAccountManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError("User must have an email")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, name, password, **extra_fields)

class UserAccount(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=200, unique=True)
    name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    username = models.CharField(max_length=200, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=200)
    date_of_birth = models.DateField(null=True)
    date_of_hire = models.DateField(auto_now=True)
    position_id = models.ForeignKey(Positions, on_delete=models.SET_NULL, null=True)
    
    STATUS_CHOICES = [
        ('working', 'Working'),
        ('quitte', 'Quitte'),
    ]

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='working',
    )
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name']

    objects = UserAccountManager()

    def getname(self):
        return self.name

    def __str__(self):
        return self.email

class Attendance(models.Model):
    attendance_id = models.AutoField(primary_key=True)
    employee_id = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    attendance_date = models.DateField()
    check_in_time = models.DateTimeField()
    check_out_time = models.DateTimeField()
    
    STATUS_CHOICES = [
        ('ontime', 'OnTime'),
        ('late', 'Late'),
        ('absent', 'Absent'),
    ]
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='ontime',
    )

class Department(models.Model):
    department_id = models.AutoField(primary_key=True)
    department_name = models.CharField(max_length=200)
    manager = models.ForeignKey(UserAccount, on_delete=models.SET_NULL, null=True)

class Leave_Type(models.Model):
    leave_type_id = models.AutoField(primary_key=True)
    leave_type = models.CharField(max_length=200)
    
    def __str__(self):
        return self.leave_type
    
class Leave(models.Model):
    leave_id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    leave_type_id = models.ForeignKey(Leave_Type, on_delete=models.SET_NULL, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.CharField(max_length=500)
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('reject', 'Reject'),
    ]
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
    )

    def __str__(self):
        return str(self.employee)


