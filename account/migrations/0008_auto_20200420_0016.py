# Generated by Django 3.0.5 on 2020-04-20 00:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cloth', '0003_auto_20200419_1849'),
        ('account', '0007_auto_20200419_1855'),
    ]

    operations = [
        migrations.AlterField(
            model_name='engage_list',
            name='cloth_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='cloth_engage', to='cloth.Cloth_type'),
        ),
        migrations.AlterField(
            model_name='engage_list',
            name='color',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='color_engage', to='cloth.Color'),
        ),
    ]
