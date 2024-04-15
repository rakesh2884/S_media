import re

from django.core.exceptions import ValidationError
from django.core.mail import send_mail

from s_media.settings import EMAIL_HOST_USER


def validate_password(value):
    if len(value) < 8:
        raise ValidationError("Make sure your password \
                              is at lest 8 letters")
    elif not re.search('[A-Z]', value):
        raise ValidationError("Make sure your password has a \
                               capital letter in it")
    elif not re.search('[^a-zA-Z0-9]', value):
        raise ValidationError("The password should have \
                               atleast one special symbol")
    elif not re.search('[0-9]', value):
        raise ValidationError("Make sure your password has a number in it")
    else:
        return value


def check_forgot_field(data):
    required_fields = ['new_password', 'confirm_password']
    for field in required_fields:
        if field not in data:
            return False
    return True


def confirm_password_check(password, confirm_password):
    if password == confirm_password:
        return True
    else:
        return False


def send_email(subject, message, email):
    email_from = EMAIL_HOST_USER
    recipient_list = [email, ]
    send_mail(subject, message, email_from, recipient_list)
