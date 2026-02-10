from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.deconstruct import deconstructible


@deconstructible
class TargetPriceValidator:
    pass