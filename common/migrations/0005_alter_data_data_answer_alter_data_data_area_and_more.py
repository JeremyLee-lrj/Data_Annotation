# Generated by Django 4.2.8 on 2023-12-25 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0004_alter_data_data_mission_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='data_answer',
            field=models.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='data_area',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='data_background',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='data_keyword',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='data_question',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='other',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='dataset_source',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='dataset_task_type',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='expert',
            name='expert_area',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='mission',
            name='mission_area',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='mission',
            name='mission_notice',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='mission',
            name='mission_original_id',
            field=models.IntegerField(null=True),
        ),
    ]
