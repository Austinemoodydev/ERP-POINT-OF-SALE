import django.db.models.deletion
from django.db import migrations, models


def set_branch_codes(apps, schema_editor):
    Branch = apps.get_model('core', 'Branch')
    for i, branch in enumerate(Branch.objects.all(), start=1):
        branch.code = f'BR{str(i).zfill(3)}'
        branch.save()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_notification'),
    ]

    operations = [

        migrations.AddField(
            model_name='branch',
            name='code',
            field=models.CharField(
                blank=True,
                max_length=20,
                unique=False,    # ← temporarily off
                default=''
            ),
        ),

        migrations.RunPython(
            set_branch_codes,
            reverse_code=migrations.RunPython.noop
        ),

        migrations.AlterField(
            model_name='branch',
            name='code',
            field=models.CharField(
                blank=True,
                max_length=20,
                unique=True,     # ← now enforced after data is filled
            ),
        ),

        migrations.AddField(
            model_name='branch',
            name='manager_name',
            field=models.CharField(
                blank=True,
                max_length=255,
                default=''
            ),
        ),

        migrations.AlterField(
            model_name='branch',
            name='address',
            field=models.TextField(blank=True),
        ),

        migrations.AlterField(
            model_name='branch',
            name='company',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to='core.company'
            ),
        ),

        migrations.AlterField(
            model_name='branch',
            name='email',
            field=models.EmailField(
                blank=True,
                max_length=254
            ),
        ),

        migrations.AlterField(
            model_name='branch',
            name='phone',
            field=models.CharField(
                blank=True,
                max_length=50
            ),
        ),

    ]
