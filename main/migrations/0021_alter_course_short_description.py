# Generated by Django 4.0.4 on 2022-05-14 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_delete_article_course_short_description_delete_paidc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='short_description',
            field=models.CharField(max_length=200),
        ),
    ]