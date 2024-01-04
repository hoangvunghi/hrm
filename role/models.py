from django.db import models

class Role(models.Model):
    RoleID=models.AutoField(primary_key=True)
    RoleName=models.CharField(max_length=200)
    