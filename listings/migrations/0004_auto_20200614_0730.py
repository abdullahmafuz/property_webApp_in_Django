# Generated by Django 3.0.6 on 2020-06-14 07:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('realtors', '0002_auto_20200529_1809'),
        ('listings', '0003_auto_20200614_0718'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='realtor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='realtors.Realtor'),
        ),
    ]
