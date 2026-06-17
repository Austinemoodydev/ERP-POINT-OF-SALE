import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0001_initial'),
        ('core', '0005_branchrole'),
    ]

    operations = [
        migrations.AddField(
            model_name='journalentry',
            name='branch',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to='core.branch'
            ),
        ),
        migrations.AddField(
            model_name='generalledger',
            name='branch',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to='core.branch'
            ),
        ),
    ]
