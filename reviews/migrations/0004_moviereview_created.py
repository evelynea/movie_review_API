# Generated by Django 5.1.1 on 2024-10-03 00:19

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reviews", "0003_alter_moviereview_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="moviereview",
            name="created",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]
