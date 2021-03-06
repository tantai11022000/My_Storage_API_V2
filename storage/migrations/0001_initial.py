# Generated by Django 3.2.12 on 2022-04-14 08:54

from django.db import migrations, models
import django.db.models.deletion
import storage.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('code', models.CharField(max_length=200, unique=True)),
                ('barcode', models.CharField(blank=True, max_length=200)),
                ('barcode_img', models.ImageField(blank=True, null=True, upload_to=storage.models.locate_barcode_img_upload)),
                ('quantity', models.CharField(max_length=200)),
                ('price', models.CharField(max_length=200)),
                ('desc', models.TextField(blank=True)),
                ('out_of_stock', models.BooleanField(default=False)),
                ('size', models.CharField(max_length=100, unique=True)),
                ('color', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='TypeGoods',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ImgGoods',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(blank=True, null=True, upload_to=storage.models.locate_img_upload)),
                ('codeGoods', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='list_img', to='storage.goods')),
            ],
        ),
        migrations.AddField(
            model_name='goods',
            name='kind',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='storage.typegoods'),
        ),
    ]
