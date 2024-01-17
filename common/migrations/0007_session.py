# Generated by Django 4.2.8 on 2024-01-16 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0006_alter_data_data_area_alter_data_data_background_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Session',
            fields=[
                ('session_id', models.AutoField(primary_key=True, serialize=False)),
                ('session_username', models.TextField()),
                ('session_usertype', models.TextField()),
                ('session_last_login_year', models.DateTimeField(null=True)),
                ('session_last_login_month', models.DateTimeField(null=True)),
                ('session_status', models.IntegerField()),
            ],
        ),
    ]