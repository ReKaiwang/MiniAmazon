# Generated by Django 2.2 on 2019-04-25 00:03

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='orders',
            fields=[
                ('shipid', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(default='InWareHouse', max_length=256)),
                ('userid', models.IntegerField()),
                ('addressx', models.IntegerField()),
                ('addressy', models.IntegerField()),
                ('upsid', models.CharField(blank=True, max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='placed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('packageid', models.IntegerField()),
                ('message', django.contrib.postgres.fields.jsonb.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='topack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('packageid', models.IntegerField()),
                ('message', django.contrib.postgres.fields.jsonb.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='truck',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shipid', models.IntegerField(blank=True)),
                ('truckid', models.IntegerField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='upsack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ack', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='upsseq',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seqnum', models.IntegerField()),
                ('message', django.contrib.postgres.fields.jsonb.JSONField()),
                ('time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='wareHouse',
            fields=[
                ('productid', models.AutoField(primary_key=True, serialize=False)),
                ('productname', models.CharField(max_length=256)),
                ('description', models.CharField(max_length=256)),
                ('count', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='worldack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ack', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='worldseq',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seqnum', models.IntegerField()),
                ('message', django.contrib.postgres.fields.jsonb.JSONField()),
                ('time', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
