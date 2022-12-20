from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _



def validate_machine_name(value):
    """Prevent some illegal characters in part names."""
    for c in ['|', '#', '$', '{', '}']:
        if c in str(value):
            raise ValidationError(
                _('Invalid character in part name')
            )

def validate_check_item_name(value):
    """Prevent some illegal characters in part names."""
    for c in ['|', '#', '$', '{', '}']:
        if c in str(value):
            raise ValidationError(
                _('Invalid character in part name')
            )