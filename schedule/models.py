import logging
from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
logger = logging.getLogger("premis")

class Period(models.Model):
    class Meta:
        pass

        name = 