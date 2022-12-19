import logging

import premis.helpers
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


from error_report.models import Error
from mptt.exceptions import InvalidMove
from mptt.models import MPTTModel, TreeForeignKey


logger = logging.getLogger("premis")

class PremisTree(MPTTModel):
    """Provides an abstracted self-referencing tree model for data categories.

    - Each Category has one parent Category, which can be blank (for a top-level Category).
    - Each Category can have zero-or-more child Categor(y/ies)

    Attributes:
        name: brief name
        description: longer form description
        parent: The item immediately above this one. An item with a null parent is a top-level item
    """

    def api_instance_filters(self):
        """Instance filters for InvenTreeTree models."""
        return {
            'parent': {
                'exclude_tree': self.pk,
            }
        }

    def save(self, *args, **kwargs):
        """Custom save method for InvenTreeTree abstract model"""

        try:
            super().save(*args, **kwargs)
        except InvalidMove:
            # Provide better error for parent selection
            raise ValidationError({
                'parent': _("Invalid choice"),
            })

        # Re-calculate the 'pathstring' field
        pathstring = premis.helpers.constructPathString(
            [item.name for item in self.path]
        )

        if pathstring != self.pathstring:
            self.pathstring = pathstring
            super().save(force_update=True)

    class Meta:
        """Metaclass defines extra model properties."""

        abstract = True

        # Names must be unique at any given level in the tree
        unique_together = ('name', 'parent')

    class MPTTMeta:
        """Set insert order."""
        order_insertion_by = ['name']

    name = models.CharField(
        blank=False,
        max_length=100,
        verbose_name=_("Name"),
        help_text=_("Name"),
    )

    description = models.CharField(
        blank=True,
        max_length=250,
        verbose_name=_("Description"),
        help_text=_("Description (optional)")
    )

    # When a category is deleted, graft the children onto its parent
    parent = TreeForeignKey('self',
                            on_delete=models.DO_NOTHING,
                            blank=True,
                            null=True,
                            verbose_name=_("parent"),
                            related_name='children')

    # The 'pathstring' field is calculated each time the model is saved
    pathstring = models.CharField(
        blank=True,
        max_length=250,
        verbose_name=_('Path'),
        help_text=_('Path')
    )

    @property
    def item_count(self):
        """Return the number of items which exist *under* this node in the tree.

        Here an 'item' is considered to be the 'leaf' at the end of each branch,
        and the exact nature here will depend on the class implementation.

        The default implementation returns zero
        """
        return 0

    def getUniqueParents(self):
        """Return a flat set of all parent items that exist above this node.

        If any parents are repeated (which would be very bad!), the process is halted
        """
        return self.get_ancestors()

    def getUniqueChildren(self, include_self=True):
        """Return a flat set of all child items that exist under this node.

        If any child items are repeated, the repetitions are omitted.
        """
        return self.get_descendants(include_self=include_self)

    @property
    def has_children(self):
        """True if there are any children under this item."""
        return self.getUniqueChildren(include_self=False).count() > 0

    def getAcceptableParents(self):
        """Returns a list of acceptable parent items within this model Acceptable parents are ones which are not underneath this item.

        Setting the parent of an item to its own child results in recursion.
        """
        contents = ContentType.objects.get_for_model(type(self))

        available = contents.get_all_objects_for_this_type()

        # List of child IDs
        childs = self.getUniqueChildren()

        acceptable = [None]

        for a in available:
            if a.id not in childs:
                acceptable.append(a)

        return acceptable

    @property
    def parentpath(self):
        """Get the parent path of this category.

        Returns:
            List of category names from the top level to the parent of this category
        """
        return [a for a in self.get_ancestors()]

    @property
    def path(self):
        """Get the complete part of this category.

        e.g. ["Top", "Second", "Third", "This"]

        Returns:
            List of category names from the top level to this category
        """
        return self.parentpath + [self]

    def __str__(self):
        """String representation of a category is the full path to that category."""
        return "{path} - {desc}".format(path=self.pathstring, desc=self.description)

@receiver(pre_delete, sender=PremisTree, dispatch_uid='tree_pre_delete_log')
def before_delete_tree_item(sender, instance, using, **kwargs):
    """Receives pre_delete signal from InvenTreeTree object.

    Before an item is deleted, update each child object to point to the parent of the object being deleted.
    """
    # Update each tree item below this one
    for child in instance.children.all():
        child.parent = instance.parent
        child.save()

# @receiver(post_save, sender=Error, dispatch_uid='error_post_save_notification')
# def after_error_logged(sender, instance: Error, created: bool, **kwargs):
#     """Callback when a server error is logged.

#     - Send a UI notification to all users with staff status
#     """

#     if created:
#         try:
#             import common.notifications

#             users = get_user_model().objects.filter(is_staff=True)

#             link = premis.helpers.construct_absolute_url(
#                 reverse('admin:error_report_error_change', kwargs={'object_id': instance.pk})
#             )

#             context = {
#                 'error': instance,
#                 'name': _('Server Error'),
#                 'message': _('An error has been logged by the server.'),
#                 'link': link
#             }

#             common.notifications.trigger_notification(
#                 instance,
#                 'inventree.error_log',
#                 context=context,
#                 targets=users,
#                 delivery_methods=set([common.notifications.UIMessageNotification]),
#             )

#         except Exception as exc:
#             """We do not want to throw an exception while reporting an exception"""
#             logger.error(exc)