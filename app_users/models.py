from django.db import models
from django.contrib.auth.models import User


class UserAdditional(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="owner")
    fullname = models.CharField(max_length=40, verbose_name="full_name")
    phone = models.CharField(max_length=11, blank=True, null=True, verbose_name="phone", unique=True)
    otp_verify = models.BooleanField(default=False, verbose_name="Phone Number Verify Status")
    opt_expire_date = models.DateTimeField(null=True, blank=True, verbose_name="OTP Expire Date")

    def __str__(self):
        return self.fullname
