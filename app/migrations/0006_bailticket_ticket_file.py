# Generated by Django 5.0.1 on 2024-06-03 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_bailticket'),
    ]

    operations = [
        migrations.AddField(
            model_name='bailticket',
            name='ticket_file',
            field=models.FileField(blank=True, upload_to='static/files'),
        ),
    ]
