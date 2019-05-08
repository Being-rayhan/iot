from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class User(AbstractUser):
    validator = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+8801XXXXXXXXX'. Up to 15 digits allowed.")
    contact_number = models.CharField(validators=[validator], max_length=17, blank=True)
    orgs = models.ForeignKey('tenants.Organization', on_delete=models.SET_NULL, null=True)
    is_client = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Organization(models.Model):
    name = models.CharField(max_length=100)

    inserted_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    modified_by = models.ForeignKey('tenants.User', on_delete=models.SET_NULL, null=True, related_name='organizations')


    class Meta:
        verbose_name_plural = "     Organizations"


    def __str__(self):
        return self.name

class Org(models.Model):
    num = models.CharField( max_length=17, blank=True)
    test_field = models.IntegerField()

    def __str__(self):
        return self.num