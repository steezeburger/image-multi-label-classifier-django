# Generated by Django 4.0 on 2022-05-27 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_label_options_alter_label_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='filename',
            field=models.CharField(db_index=True, help_text='The filename of the image.', max_length=1024, unique=True),
        ),
    ]
