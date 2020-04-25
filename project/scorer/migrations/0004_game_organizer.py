# Generated by Django 3.0.5 on 2020-04-25 09:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('scorer', '0003_auto_20200425_2029'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='organizer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='organizer', to=settings.AUTH_USER_MODEL),
        ),
    ]
