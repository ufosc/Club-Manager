# Generated by Django 4.2.17 on 2024-12-25 19:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        (
            "clubs",
            "0010_remove_event_unique_event_name_per_timerange_per_club_and_more",
        ),
    ]

    operations = [
        migrations.DeleteModel(
            name="QRCode",
        ),
    ]