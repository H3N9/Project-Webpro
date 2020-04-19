# Generated by Django 3.0.5 on 2020-04-19 18:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cloth', '0002_auto_20200417_1303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cloth_in_stock',
            name='cloth_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cloth_stock', to='cloth.Cloth_type'),
        ),
        migrations.AlterField(
            model_name='cloth_in_stock',
            name='color',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='color_stock', to='cloth.Color'),
        ),
    ]
