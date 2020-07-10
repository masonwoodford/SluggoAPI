# Generated by Django 3.0.8 on 2020-07-10 00:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_ticket'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='completed',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='due_date',
            field=models.DateField(blank=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='started',
            field=models.DateTimeField(blank=True),
        ),
    ]
