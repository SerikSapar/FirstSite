# Generated by Django 4.0.4 on 2022-05-04 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_course_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('time', models.DateTimeField()),
                ('logo', models.ImageField(upload_to='static')),
                ('view', models.IntegerField(default=0)),
                ('show_count', models.IntegerField(default=0)),
                ('short_description', models.CharField(max_length=200)),
            ],
        ),
    ]
