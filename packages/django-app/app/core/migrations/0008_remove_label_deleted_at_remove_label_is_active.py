# Generated by Django 4.0 on 2022-06-02 04:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_remove_labeledimage_deleted_at_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='label',
            name='deleted_at',
        ),
        migrations.RemoveField(
            model_name='label',
            name='is_active',
        ),
    ]
