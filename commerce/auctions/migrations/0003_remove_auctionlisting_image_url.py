# Generated by Django 5.1.5 on 2025-04-29 14:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_category_auctionlisting_imageurl_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auctionlisting',
            name='image_url',
        ),
    ]
