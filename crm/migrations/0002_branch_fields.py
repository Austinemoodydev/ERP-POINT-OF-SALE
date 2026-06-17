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


def set_crm_branches(apps, schema_editor):
    LoyaltyAccount = apps.get_model('crm', 'LoyaltyAccount')
    SupportTicket = apps.get_model('crm', 'SupportTicket')
    branch = get_default_branch(apps)

    for loyalty_account in LoyaltyAccount.objects.filter(branch__isnull=True).select_related('customer'):
        loyalty_account.branch_id = loyalty_account.customer.branch_id or branch.id
        loyalty_account.save(update_fields=['branch'])

    for ticket in SupportTicket.objects.filter(branch__isnull=True).select_related('customer'):
        ticket.branch_id = ticket.customer.branch_id or branch.id
        ticket.save(update_fields=['branch'])


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_branchrole'),
        ('sales', '0002_customer_branch'),
        ('crm', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='loyaltyaccount',
            name='branch',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to='core.branch'
            ),
        ),
        migrations.AddField(
            model_name='supportticket',
            name='branch',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to='core.branch'
            ),
        ),
        migrations.RunPython(
            set_crm_branches,
            reverse_code=migrations.RunPython.noop
        ),
        migrations.AlterField(
            model_name='loyaltyaccount',
            name='branch',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to='core.branch'
            ),
        ),
        migrations.AlterField(
            model_name='supportticket',
            name='branch',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to='core.branch'
            ),
        ),
    ]
