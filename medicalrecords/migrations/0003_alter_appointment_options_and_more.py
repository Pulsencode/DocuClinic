# Generated by Django 5.1.1 on 2024-11-09 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicalrecords', '0002_rename_doctor_appointment_physician_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='appointment',
            options={'ordering': ['date', 'time']},
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='appointment_datetime',
        ),
        migrations.AddField(
            model_name='appointment',
            name='date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='appointment',
            name='time',
            field=models.TimeField(null=True),
        ),
    ]
