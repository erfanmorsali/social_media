# Generated by Django 3.1.3 on 2020-11-05 19:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social_media_posts', '0004_auto_20201104_1515'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='postcomment',
            options={'ordering': ('-created',), 'verbose_name': ('کامنت',), 'verbose_name_plural': 'کامنت ها'},
        ),
    ]
