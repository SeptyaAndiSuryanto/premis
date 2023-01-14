import logging

from mptt.managers import TreeManager
from mptt.models import MPTTModel, TreeForeignKey

from django.contrib.auth.models import User
from django.db import models, transaction
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from premis.models import PremisTree
import premis.validators as validators
import premis.helpers as helpers


# Create your models here.
logger = logging.getLogger("premis")

class MachineCategory(PremisTree):
    """MachineCategory provides hierarchical organization of Machine objects.

    Attributes:
        name: Name of this category
        parent: Parent category
    """
    def delete(self, *args, **kwargs):
        """Custom model deletion routine, which updates any child categories or parts.

        This must be handled within a transaction.atomic(), otherwise the tree structure is damaged
        """
        with transaction.atomic():

            parent = self.parent
            tree_id = self.tree_id

            # Update each part in this category to point to the parent category
            for p in self.parts.all():
                p.category = self.parent
                p.save()

            # Update each child category
            for child in self.children.all():
                child.parent = self.parent
                child.save()

            super().delete(*args, **kwargs)

            if parent is not None:
                # Partially rebuild the tree (cheaper than a complete rebuild)
                MachineCategory.objects.partial_rebuild(tree_id)
            else:
                MachineCategory.objects.rebuild()

    def get_absolute_url(self):
        """Return the web URL associated with the detail view for this MachineCategory instance"""
        return reverse('category-detail', kwargs={'pk': self.id})

    class Meta:
        verbose_name = _("Machine Category")
        verbose_name_plural = _("Machine Categories")
    
    def get_machine(self, cascade=True) -> models.QuerySet:
        """Return a queryset for all Machine under this category.

        Args:
            cascade (bool, optional): If True, also look under subcategories. Defaults to True.

        Returns:
            set[Machine]: All matching Machine
        """
        if cascade:
            """Select any Machine which exist in this category or any child categories."""
            queryset = Machine.objects.filter(category__in=self.getUniqueChildren(include_self=True))
        else:
            queryset = Machine.objects.filter(category=self.pk)

        return queryset

    def machine_count(self, cascade=True, active=False):
        """Return the total part count under this category (including children of child categories)."""
        query = self.get_machine(cascade=cascade)

        if active:
            query = query.filter(active=True)

        return query.count()


class MachineManager(TreeManager):
    """Defines a custom object manager for the Part model.

    The main purpose of this manager is to reduce the number of database hits,
    as the Part model has a large number of ForeignKey fields!
    """

    def get_queryset(self):
        """Perform default prefetch operations when accessing Part model from the database"""
        return super().get_queryset().prefetch_related(
            'category',
            'category__parent',
        )


class Machine(models.Model):
    
    name = models.CharField(
        max_length=100, blank=False,
        help_text=_('Machine name'),
        verbose_name=_('Name'),
        validators=[validators.validate_machine_name]
    )

    category = TreeForeignKey(
        MachineCategory, related_name='machines',
        null=True, blank=True,
        on_delete=models.DO_NOTHING,
        verbose_name=_('Category'),
        help_text=_('Machine category')
    )

    IPN = models.CharField(
        max_length=30, blank=True, null=True,
        verbose_name=_('IPN'),
        help_text=_('Internal Part Number')
    )

    description = models.CharField(
        blank=True,
        max_length=250,
        verbose_name=_("Description"),
        help_text=_("Description (optional)")
    )

    active = models.BooleanField(
        default=True,
        verbose_name=_('Active'),
        help_text=_('Is this machine active?'))
    
    creation_date = models.DateField(auto_now_add=True, editable=False, blank=True, null=True, verbose_name=_('Creation Date'))

    creation_user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('Creation User'), related_name='machine_created')

    def format_barcode(self, **kwargs):
        """Return a JSON string for formatting a barcode for this Part object."""
        return helpers.MakeBarcode(
            "machine",
            self.id,
            {
                "name": self.full_name,
                "url": reverse('api-machine-detail', kwargs={'pk': self.id}),
            },
            **kwargs
        )
    
    def __str__(self):
        """Get string representation of a Period."""
        return "{n} - {d}".format(n=self.category.name, d=self.name)

