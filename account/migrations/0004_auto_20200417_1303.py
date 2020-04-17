# Generated by Django 3.0.5 on 2020-04-17 13:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cloth', '0002_auto_20200417_1303'),
        ('account', '0003_auto_20200416_2312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='engage_list',
            name='cloth_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='cloth.Cloth_type'),
        ),
        migrations.AlterField(
            model_name='engage_list',
            name='color',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='cloth.Color'),
        ),
    ]