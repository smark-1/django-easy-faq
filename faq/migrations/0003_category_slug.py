# Generated by Django 3.1.4 on 2021-02-18 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faq', '0002_auto_20210217_2207'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(default='slug', unique=True),
            preserve_default=False,
        ),
    ]
