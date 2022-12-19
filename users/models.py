import logging
from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
logger = logging.getLogger("premis")

class RuleSet(models.Model):
    RULESET_CHOICE = [
        ('admin', _('Admin')),
        ()
    ]
    class Meta:
        pass