# Generated by Django 2.1.1 on 2018-09-13 13:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0002_courseorg_catgory'),
    ]

    operations = [
        migrations.RenameField(
            model_name='courseorg',
            old_name='catgory',
            new_name='category',
        ),
    ]