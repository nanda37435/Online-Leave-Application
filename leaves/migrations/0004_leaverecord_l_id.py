# Generated by Django 2.2.5 on 2020-08-08 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaves', '0003_auto_20200807_1924'),
    ]

    operations = [
        migrations.AddField(
            model_name='leaverecord',
            name='l_id',
            field=models.CharField(default=None, max_length=100),
        ),
    ]