from django.contrib import admin

from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field
import import_export.widgets as widgets

from premis.admin import PremisResource
import machine.models as models

# Register your models here.
class MachineResource(PremisResource):
    """Class for managing Part data import/export."""

    # ForeignKey fields
    category = Field(attribute='category', widget=widgets.ForeignKeyWidget(models.MachineCategory))

    category_name = Field(attribute='category__name', readonly=True)


    class Meta:
        """Metaclass definition"""
        model = models.Machine
        skip_unchanged = True
        report_skipped = False
        clean_model_instances = True
        exclude = [
            'lft', 'rght', 'tree_id', 'level',
        ]

    def get_queryset(self):
        """Prefetch related data for quicker access."""
        query = super().get_queryset()
        query = query.prefetch_related(
            'category',
        )

        return query

    def after_import(self, dataset, result, using_transactions, dry_run, **kwargs):
        """Rebuild MPTT tree structure after importing Part data"""

        super().after_import(dataset, result, using_transactions, dry_run, **kwargs)

        # Rebuild the Part tree(s)
        models.Machine.objects.rebuild()


class MachineAdmin(ImportExportModelAdmin):
    """Admin class for the Part model"""

    resource_class = MachineResource

    list_display = ('name', 'description', 'category')

    list_filter = ('active',)

    search_fields = ('name', 'description', 'category__name', 'category__description', 'IPN')

    autocomplete_fields = [
        'category',
    ]


class MachineCategoryResource(PremisResource):
    """Class for managing PartCategory data import/export."""

    parent = Field(attribute='parent', widget=widgets.ForeignKeyWidget(models.MachineCategory))

    parent_name = Field(attribute='parent__name', readonly=True)

    class Meta:
        """Metaclass definition"""
        model = models.MachineCategory
        skip_unchanged = True
        report_skipped = False
        clean_model_instances = True

        exclude = [
            # Exclude MPTT internal model fields
            'lft', 'rght', 'tree_id', 'level',
            'metadata',
        ]

    def after_import(self, dataset, result, using_transactions, dry_run, **kwargs):
        """Rebuild MPTT tree structure after importing PartCategory data"""

        super().after_import(dataset, result, using_transactions, dry_run, **kwargs)

        # Rebuild the PartCategory tree(s)
        models.MachineCategory.objects.rebuild()


class MachineCategoryAdmin(ImportExportModelAdmin):
    """Admin class for the PartCategory model"""

    resource_class = MachineCategoryResource

    list_display = ('name', 'pathstring', 'description')

    search_fields = ('name', 'description')

    autocomplete_fields = ('parent',)


admin.site.register(models.Machine, MachineAdmin)
admin.site.register(models.MachineCategory, MachineCategoryAdmin)
