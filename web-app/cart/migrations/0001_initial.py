# Generated by Django 2.2 on 2019-04-25 00:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='carts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productid', models.IntegerField(choices=[(1, 'Apple'), (2, 'Google'), (3, 'Str.8 Yanzu'), (4, 'Yamahui'), (5, 'Water Like Man')])),
                ('userid', models.IntegerField()),
                ('count', models.IntegerField()),
                ('status', models.CharField(blank=True, default='InOrder', max_length=256)),
                ('ship', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='order.orders')),
            ],
        ),
    ]