# Generated by Django 2.2.16 on 2022-07-24 01:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0007_Update_Pub_Date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-pub_date'], 'verbose_name': 'Комментарий', 'verbose_name_plural': 'Комментарии'},
        ),
    ]
