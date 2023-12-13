from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from datetime import datetime


class Department(models.Model):
    DepID = models.AutoField(primary_key=True)
    DepName = models.CharField(max_length=255)


class Position(models.Model):
    PosID = models.AutoField(primary_key=True)
    PosName = models.CharField(max_length=255)


class Employee(models.Model):
    EmpID = models.AutoField(primary_key=True)
    EmpName = models.CharField(max_length=255)
    Phone = models.CharField(max_length=15)
    HireDate = models.DateTimeField()
    BirthDate = models.DateTimeField()
    Address = models.CharField(max_length=255)
    PhotoPath = models.CharField(max_length=255)
    Email = models.EmailField()
    Salary = models.FloatField()
    role = models.BooleanField()
    DepID = models.ForeignKey(Department, on_delete=models.CASCADE)
    PosID = models.ForeignKey(Position, on_delete=models.CASCADE)
    EmpStatus = models.BooleanField()


class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("User must have an email")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user


    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        return self.create_user(email=email,password=password, **extra_fields)
    
    

class UserAccount(PermissionsMixin, AbstractBaseUser):
    UserID = models.CharField(primary_key=True, max_length=255)
    email = models.EmailField(unique=True)
    EmpID = models.ForeignKey(Employee, on_delete=models.SET_NULL,blank=True,null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)   
    # password=models.CharField(max_length=255)
    objects = UserAccountManager()
    username = models.CharField(max_length=255,unique=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ["email","UserID"] 


class LeaveType(models.Model):
    LeaveTypeID = models.AutoField(primary_key=True)
    LeaveTypeName = models.CharField(max_length=255)


class Leave(models.Model):
    LeaveID = models.AutoField(primary_key=True)
    EmpID = models.ForeignKey(Employee, on_delete=models.CASCADE)
    LeaveStartDate = models.DateTimeField()
    LeaveEndDate = models.DateTimeField()
    LeaveTypeID = models.ForeignKey(LeaveType, on_delete=models.CASCADE)
    Reason = models.CharField(max_length=500)
    LeaveStatus = models.CharField(max_length=255)


class TimeSheet(models.Model):
    TimeID = models.AutoField(primary_key=True)
    TimeIn = models.DateTimeField()
    TimeOut = models.DateTimeField()
    EmpID = models.ForeignKey(Employee, on_delete=models.CASCADE)


class Project(models.Model): 
    proj_id = models.AutoField(primary_key=True)
    proj_name = models.CharField(max_length=20)
    proj_value = models.IntegerField()
    date_start = models.DateField(auto_now=True)
    date_end = models.DateField()
    proj_description = models.CharField(max_length=200)
    manager_id = models.OneToOneField(Employee, on_delete=models.CASCADE, null=True)
    COMPLETE_CHOICES = [
        ('finished', 'Finished'),
        ('unfinished', 'Unfinished'),
    ]
    complete = models.CharField(
        max_length=20,
        choices=COMPLETE_CHOICES,
        default='unfinished',
    )

class Task(models.Model):
    # id = models.AutoField(primary_key=True)
    proj_id = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    user_id = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    description = models.TextField()

# class Task(models.Model):
#     id = models.AutoField(primary_key=True)
#     title = models.CharField(max_length=255)
#     description = models.TextField()
#     completed = models.BooleanField(default=False)
#     user_id = models.ForeignKey(UserAccount, on_delete=models.SET_NULL, null=True)
#     proj_id = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)


################################################################3
# from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
# from datetime import datetime

# class Positions(models.Model):
#     position_id = models.AutoField(primary_key=True)
#     position_name = models.CharField(max_length=200)


# class UserAccountManager(BaseUserManager):
#     def create_user(self, email, name, password=None, **extra_fields):
#         if not email:
#             raise ValueError("User must have an email")
#         email = self.normalize_email(email)
#         user = self.model(email=email, name=name, **extra_fields)
#         user.set_password(password)
#         user.save()
#         return user

# # #hàm mới
#     def create_superuser(self, email, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
        
#         return self.create_user(email=email, name='admin', password=password, **extra_fields)
# # #hàm cũ
#     # def create_superuser(self, email, password=None, **extra_fields):
#     #     extra_fields.setdefault('is_staff', True)
#     #     extra_fields.setdefault('is_superuser', True)
        
#     #     return self.create_user(email, password, **extra_fields)


    

# class UserAccount(AbstractBaseUser, PermissionsMixin):
#     user_id = models.AutoField(primary_key=True)
#     email = models.EmailField(max_length=200, unique=True)
#     name = models.CharField(max_length=200)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     username = models.CharField(max_length=200, unique=True)
#     first_name = models.CharField(max_length=50,null=True)
#     last_name = models.CharField(max_length=50,null=True)
#     phone_number = models.CharField(max_length=15,null=True)
#     address = models.CharField(max_length=200)
#     date_of_birth = models.DateField(null=True)
#     date_of_hire = models.DateField(auto_now=True)
#     position_id = models.ForeignKey(Positions, on_delete=models.SET_NULL, null=True)
    
#     STATUS_CHOICES = [
#         ('working', 'Working'),
#         ('quitte', 'Quitte'),
#     ]

#     status = models.CharField(
#         max_length=10, 
#         choices=STATUS_CHOICES,
#         default='working',
#     )
#     USERNAME_FIELD = 'username'
#     REQUIRED_FIELDS = ['email']

#     objects = UserAccountManager()

#     def getname(self):
#         return self.name

#     def __str__(self):
#         return self.email

# class Attendance(models.Model):
#     attendance_id = models.AutoField(primary_key=True)
#     employee_id = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
#     attendance_date = models.DateField(auto_now=True)
#     check_in_time = models.DateTimeField(auto_now=True)
#     check_out_time = models.DateTimeField(auto_now_add=True)
    
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

# class Department(models.Model):
#     department_id = models.AutoField(primary_key=True)
#     department_name = models.CharField(max_length=200)
#     manager = models.ForeignKey(UserAccount, on_delete=models.SET_NULL, null=True)

# class Leave_Type(models.Model):
#     leave_type_id = models.AutoField(primary_key=True)
#     leave_type = models.CharField(max_length=200)
    
#     def __str__(self):
#         return self.leave_type
    
# class Leave(models.Model):
#     leave_id = models.AutoField(primary_key=True)
#     employee = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
#     leave_type_id = models.ForeignKey(Leave_Type, on_delete=models.SET_NULL, null=True)
#     start_date = models.DateField()
#     end_date = models.DateField()
#     reason = models.CharField(max_length=500)
    
#     STATUS_CHOICES = [
#         ('pending', 'Pending'),
#         ('approved', 'Approved'),
#         ('reject', 'Reject'),
#     ]
#     status = models.CharField(
#         max_length=10,
#         choices=STATUS_CHOICES,
#         default='pending',
#     )

#     def __str__(self):
#         return str(self.employee)


# class Project(models.Model): 
#     proj_id = models.AutoField(primary_key=True)
#     proj_name = models.CharField(max_length=20)
#     proj_value = models.IntegerField()
#     date_start = models.DateField(auto_now=True)
#     date_end = models.DateField()
#     proj_description = models.CharField(max_length=200)
#     manager_id = models.OneToOneField(UserAccount, on_delete=models.CASCADE, null=True)
#     COMPLETE_CHOICES = [
#         ('finished', 'Finished'),
#         ('unfinished', 'Unfinished'),
#     ]
#     complete = models.CharField(
#         max_length=20,
#         choices=COMPLETE_CHOICES,
#         default='unfinished',
#     )

# class Task(models.Model):
#     # id = models.AutoField(primary_key=True)
#     proj_id = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
#     user_id = models.ForeignKey(UserAccount, on_delete=models.SET_NULL, null=True)
#     description = models.TextField()

# # class Task(models.Model):
# #     id = models.AutoField(primary_key=True)
# #     title = models.CharField(max_length=255)
# #     description = models.TextField()
# #     completed = models.BooleanField(default=False)
# #     user_id = models.ForeignKey(UserAccount, on_delete=models.SET_NULL, null=True)
# #     proj_id = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)
