from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from datetime import datetime
from department.models import Department
from job.models import Job
from role.models import Role


class Employee(models.Model):
    EmpID = models.AutoField(primary_key=True)
    EmpName = models.CharField(max_length=255)
    Phone = models.CharField(max_length=15,null=True)
    HireDate = models.DateField(null=True)
    BirthDate = models.DateField(null=True)
    Address = models.CharField(max_length=255,null=True)
    PhotoPath = models.ImageField(upload_to='employee_photos/', default='employee_photos/default.jpg')
    Email = models.EmailField()
    DepID = models.ForeignKey(Department, on_delete=models.SET_NULL,null=True)
    JobID = models.ForeignKey(Job, on_delete=models.SET_NULL,null=True)
    EmpStatus = models.BooleanField(default=True)
    Gender=models.CharField(max_length=12,null=True)
    RoleID=models.ForeignKey(Role,on_delete=models.SET_NULL,null=True,blank=True)
    TaxCode=models.CharField(max_length=100,null=True)
    CCCD=models.CharField(max_length=12)
    BankAccountNumer=models.CharField(max_length=50,null=True)
    BankName=models.CharField(max_length=100,null=True)
    


class UserAccountManager(BaseUserManager):
    def create_user(self, email=None, password=None, **extra_fields):
        # if not email:
        #     raise ValueError("User must have an email")
        # email = self.normalize_email(email)
        user = self.model( **extra_fields)
        user.set_password(password)
        user.save()
        return user
    # def create_superuser(self,email=None, password=None, **extra_fields):
    #     # extra_fields.setdefault('is_staff', True)
    #     # extra_fields.setdefault('is_superuser', True)
    #     return self.create_user( password=password, **extra_fields)
    def create_superuser(self, UserID, password, **extra_fields):
        employee=Employee(
            EmpID = 0,
            EmpName = 'Admin',
            HireDate = '2023-06-06',
            BirthDate = '2023-06-06',
            Address = 'a',
            PhotoPath = 'a',
            Email = 'admin',
            EmpStatus = True)
        user = self.create_user(
            UserID=UserID,
            password=password,
            UserStatus=True,
            EmpID=employee
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class UserAccount(AbstractBaseUser, PermissionsMixin):
    UserID = models.CharField(primary_key=True, max_length=255)
    EmpID = models.ForeignKey(Employee, on_delete=models.CASCADE)
    objects = UserAccountManager()
    UserStatus = models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    USERNAME_FIELD = 'UserID'
    last_login = None
    email=None
    def get_password(self):
        return self.password[21:30]


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
