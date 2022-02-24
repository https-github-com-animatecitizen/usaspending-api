# Generated by Django 2.2.17 on 2022-02-24 15:36
import partial_index
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipient', '0013_create_uei_indexes_for_performance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipientlookup',
            name='duns',
            field=models.TextField(null=True),
        ),
        migrations.AddIndex(
            model_name='recipientlookup',
            index=partial_index.PartialIndex(fields=['duns'], name='recipient_l_duns_a43c07_partial', unique=False, where=partial_index.PQ(duns__isnull=False)),
        ),
    ]
