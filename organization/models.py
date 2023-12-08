from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class SingletonModel(models.Model):
    class Meta:
        abstract = True
    @classmethod
    def load(cls):
        instance, created = cls.objects.get_or_create(pk=1)
        return instance
    def save(self, *args, **kwargs):
        self.pk = 1  
        super().save(*args, **kwargs)


class Organization(SingletonModel):
    organization_name=models.CharField(max_length=255)
    tax_id=models.CharField(max_length=255)
    number_of_employees=models.CharField(max_length=255)
    registration_employees=models.CharField(max_length=255)
    cost_center=models.CharField(max_length=255)
    phone=models.CharField(max_length=255)
    tax=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    address_stress=models.CharField(max_length=255)
    city=models.CharField(max_length=255)
    zip_postalcode=models.CharField(max_length=255)
    country=models.CharField(max_length=255)
    note=models.CharField(max_length=255)

    @classmethod
    def update_organization_info(cls, data):
        organization_instance, created = cls.objects.get_or_create(pk=1)
        for key, value in data.items():
            setattr(organization_instance, key, value)
        organization_instance.save()
        return organization_instance
