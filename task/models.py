import logging

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q, Sum, UniqueConstraint
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

import premis.validators as validators
from machine.models import Machine

# Create your models here.

logger = logging.getLogger("premis")

class Period(models.Model):

    @staticmethod
    def get_api_url():
        """Return the API URL associated with the Company model"""
        return reverse('api-period-list')

    name = models.CharField(
        verbose_name=_("Name"),
        max_length=30, blank=False,
        help_text=_("Name"),
    )

    value_in_day = models.SmallIntegerField(
        verbose_name=_("Value in day"),
        blank=False,
        help_text=_("Value in day")
    )

    def __str__(self):
        """Get string representation of a Period."""
        return "{n}".format(n=self.name)
    
    class Meta:
        ordering = ['value_in_day', ]
        constraints = [
            UniqueConstraint(fields=['name', 'value_in_day'], name='unique_name_value_in_day_pair')
        ]
        verbose_name = 'Period'
        verbose_name_plural = 'Periods'
    
    def get_absolute_url(self):
        """Get the web URL for the detail view for this Period."""
        return reverse('period-detail', kwargs={'pk': self.id})
    

class CheckItem(models.Model):

    class Meta:
        # ordering = ['value_in_day', ]
        # constraints = [
        #     UniqueConstraint(fields=['name', 'value_in_day'], name='unique_name_email_pair')
        # ]
        verbose_name = 'Check Item'
        verbose_name_plural = 'Check Items'

    name = models.CharField(
        verbose_name=_("Name"),
        max_length=100, blank=False,
        help_text=_("Name"),
        validators=[validators.validate_check_item_name]
    )

    period = models.ForeignKey(Period, related_name='check_items', on_delete=models.DO_NOTHING)

    description = models.CharField(
        blank=True,
        max_length=250,
        verbose_name=_("Description"),
        help_text=_("Description (optional)")
    )

    creation_date = models.DateField(auto_now_add=True, editable=False, blank=True, null=True, verbose_name=_('Creation Date'))

    creation_user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('Creation User'), related_name='check_item_created')

    def get_absolute_url(self):
        """Get the web URL for the detail view for this Period."""
        return reverse('check-item-detail', kwargs={'pk': self.id})
    
    def __str__(self):
        """Get string representation of a Period."""
        return "{n} - {d}".format(n=self.name, d=self.period.name)
    
    @staticmethod
    def get_api_url():
        """Return the API URL associated with the Company model"""
        return reverse('api-check-item-list')


class Task(models.Model):

    machine = models.ForeignKey(Machine, verbose_name=_("Machine"), on_delete=models.DO_NOTHING)

    item = models.ForeignKey(CheckItem, verbose_name=_("Item"), on_delete=models.DO_NOTHING)

    description = models.CharField(
        blank=True,
        max_length=250,
        verbose_name=_("Description"),
        help_text=_("Description (optional)")
    )

    creation_date = models.DateField(auto_now_add=True, editable=False, blank=True, null=True, verbose_name=_('Creation Date'))

    creation_user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('Creation User'), related_name='task_created')


    class Meta:
        constraints = [
            UniqueConstraint(fields=['machine', 'item'], name='unique_machine_item_pair')
        ]
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")

    def __str__(self):
        """Get string representation of a Period."""
        return "{n} - {d}".format(n=self.machine, d=self.item)

    def get_absolute_url(self):
        """Get the web URL for the detail view for this task."""
        return reverse('task-detail', kwargs={'pk': self.id})
