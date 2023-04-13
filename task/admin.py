from django.contrib import admin

from import_export.admin import ImportExportModelAdmin

from premis.admin import PremisResource
import task.models as models
# Register your models here.
class PeriodResource(PremisResource):
    
    class Meta:
        """Metaclass defines extra options"""
        model = models.Period
        skip_unchanged = True
        report_skipped = False
        clean_model_instances = True


class PeriodAdmin(ImportExportModelAdmin):
    """Admin class for the Company model"""

    resource_class = PeriodResource

    list_display = ('name', 'value_in_day')

    search_fields = [
        'name',
        'value_in_day',
    ]


class CheckItemResource(PremisResource):
    
    class Meta:
        """Metaclass defines extra options"""
        model = models.CheckItem
        skip_unchanged = True
        report_skipped = False
        clean_model_instances = True


class CheckItemAdmin(ImportExportModelAdmin):
    """Admin class for the Company model"""

    resource_class = CheckItemResource

    list_display = ('id','name', 'period', 'description')

    search_fields = [
        'name',
        'description',
    ]


class TaskResource(PremisResource):
    
    class Meta:
        """Metaclass defines extra options"""
        model = models.Task
        skip_unchanged = True
        report_skipped = False
        clean_model_instances = True


class TaskAdmin(ImportExportModelAdmin):
    """Admin class for the Company model"""

    resource_class = TaskResource

    list_display = ('id','machine', 'item', 'description')

    search_fields = [
        'machine',
        'item',
        'description',
    ]


class RecordResource(PremisResource):
    
    class Meta:
        """Metaclass defines extra options"""
        model = models.Record
        skip_unchanged = True
        report_skipped = False
        clean_model_instances = True


class RecordAdmin(ImportExportModelAdmin):
    """Admin class for the Company model"""

    resource_class = RecordResource

    list_display = ('id','task', 'remarks', 'creation_date','creation_user')

    search_fields = [
        'task',
        'remarks',
        'creation_date',
    ]


admin.site.register(models.Period, PeriodAdmin)
admin.site.register(models.CheckItem, CheckItemAdmin)
admin.site.register(models.Task, TaskAdmin)
admin.site.register(models.Record, RecordAdmin)
