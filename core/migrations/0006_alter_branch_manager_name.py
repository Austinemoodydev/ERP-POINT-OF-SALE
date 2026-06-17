from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_branchrole'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch',
            name='manager_name',
            field=models.CharField(
                blank=True,
                max_length=255
            ),
        ),
    ]
