import django.db.models.deletion
from django.db import migrations, models


def get_default_branch(apps):
    Branch = apps.get_model('core', 'Branch')
    branch, _ = Branch.objects.get_or_create(
        code='HO',
        defaults={
            'name': 'Head Office',
            'phone': '',
            'email': '',
            'address': '',
            'manager_name': '',
            'active': True,
        }
    )
    return branch


def set_customer_branches(apps, schema_editor):
    Customer = apps.get_model('sales', 'Customer')
    branch = get_default_branch(apps)
    Customer.objects.filter(branch__isnull=True).update(branch=branch)


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_branchrole'),
        ('sales', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='branch',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to='core.branch'
            ),
        ),
        migrations.RunPython(
            set_customer_branches,
            reverse_code=migrations.RunPython.noop
        ),
        migrations.AlterField(
            model_name='customer',
            name='branch',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to='core.branch'
            ),
        ),
    ]
