from datetime import datetime, timedelta
from random import randint
import config.settings
from config.tools.datetime_tools import datetime_difference_from_now, now_tehran
from django.core.exceptions import ValidationError
from config.tools.otp_tools import send_otp
from .models import UserAdditional
from django.contrib.auth.models import User
from rest_framework import serializers
from config.tools.utilities import validate_phone_number, validate_name, password_generator, is_it_numeric


class UserSerializer(serializers.Serializer):
    fullname = serializers.CharField(required=True, max_length=40, min_length=2)
    phone = serializers.CharField(max_length=11, min_length=11, required=True)

    @staticmethod
    def validate_fullname(attrs):
        if validate_name(attrs, maxlength=40, minlength=2, english=False):
            return attrs
        else:
            raise ValidationError("invalid fullname")

    @staticmethod
    def validate_phone(attrs):
        # Validate Phone Format
        if validate_phone_number(attrs):
            # Unique validation
            if User.objects.filter(username__exact=attrs).count() != 0:
                # raise ValidationError(JsonResponse({'detail': "username already exist"}, status=status.HTTP_409_CONFLICT))
                raise ValidationError("username already exist")
            return attrs
        else:
            raise ValidationError("invalid phone number")

    def create(self, validated_data):
        # get data
        received_phone = validated_data.get('phone')

        # create New user
        new_user = User.objects.create(username=received_phone, password=password_generator(10))
        new_user.save()
        # append Additional to User
        useradditional_creator = UserAdditional.objects.create(
            owner=new_user,
            fullname=validated_data.get('fullname'),
            phone=validated_data.get('phone'),
        )
        useradditional_creator.save()

        return new_user

    # edit users
    def update(self, instance, validated_data):
        pass


class OtpSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=11, min_length=11, required=True)

    @staticmethod
    def validate_phone(attrs):
        # Validate Phone Format
        if validate_phone_number(attrs):
            # Unique validation
            if User.objects.filter(username__exact=attrs).count() == 0:
                raise ValidationError("user does not exist")
            return attrs
        else:
            raise ValidationError("invalid phone number")

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        received_phone = validated_data.get('phone')
        the_user = User.objects.filter(username__exact=received_phone).first()
        otp_expire_time: datetime = the_user.useradditional.opt_expire_date

        if otp_expire_time:  # if expire time exist
            remaining_time = datetime_difference_from_now(otp_expire_time)
            if remaining_time > 0:
                raise ValidationError(f"cannot request new otp until {remaining_time}s remaining")

        # set new OTP and send expire time
        # set new expire time
        new_otp_expire_time = now_tehran() + timedelta(minutes=config.settings.OTP_EXPIRE_TIME)
        the_user.useradditional.opt_expire_date = new_otp_expire_time
        the_user.useradditional.save()
        # create and send OTP
        otp = str(randint(100000, 999999))
        send_otp(template_name="AIC", otp_code=otp, receiver_phone=received_phone)
        # set password
        the_user = User.objects.get(username__exact=received_phone)
        the_user.set_password(otp)
        the_user.save()
        return validated_data

        # remaining_time = (otp_expire_time - datetime.now()).total_seconds()


class JwtSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=11, min_length=11, required=True)
    otp = serializers.CharField(max_length=6, min_length=6, required=True)

    @staticmethod
    def validate_phone(attrs):
        # Validate Phone Format
        if validate_phone_number(attrs):
            # Unique validation
            if User.objects.filter(username__exact=attrs).count() == 0:
                raise ValidationError("user does not exist")
            return attrs
        else:
            raise ValidationError("invalid phone number")

    @staticmethod
    def validate_otp(attrs):
        if is_it_numeric(attrs) and len(attrs) == 6:
            return attrs
        raise ValidationError("invalid otp (otp must be 6 digits)")

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
