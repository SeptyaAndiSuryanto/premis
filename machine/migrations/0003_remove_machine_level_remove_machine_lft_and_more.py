# Generated by Django 4.1.3 on 2022-12-19 09:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('machine', '0002_alter_machinecategory_options_machine'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='machine',
            name='level',
        ),
        migrations.RemoveField(
            model_name='machine',
            name='lft',
        ),
        migrations.RemoveField(
            model_name='machine',
            name='rght',
        ),
        migrations.RemoveField(
            model_name='machine',
            name='tree_id',
        ),
    ]
