# Generated by Django 4.0.4 on 2022-05-04 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_shi'),
    ]

    operations = [
        migrations.AddField(
            model_name='shi',
            name='description',
            field=models.CharField(default=0, max_length=500),
            preserve_default=False,
        ),
    ]
