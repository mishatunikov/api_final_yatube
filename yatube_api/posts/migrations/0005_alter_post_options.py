# Generated by Django 3.2.16 on 2025-02-15 08:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_auto_20250214_1704'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('-pub_date',)},
        ),
    ]
