import re
from django.core.exceptions import ValidationError

        
def validate_password(value):
    if len(value)<8:
        raise ValidationError("Make sure your password is at lest 8 letters")
    elif not re.search('[A-Z]',value):
        raise ValidationError("Make sure your password has a capital letter in it")
    elif not re.search('[^a-zA-Z0-9]',value):
        raise ValidationError("The password should have atleast one special symbol")
    elif not re.search('[0-9]',value):
        raise ValidationError("Make sure your password has a number in it")
    else:
        return value
                
        