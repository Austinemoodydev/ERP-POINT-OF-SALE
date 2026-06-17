from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_remove_productserial_action_and_more'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.DeleteModel(
                    name='BranchTransferItem',
                ),
                migrations.DeleteModel(
                    name='BranchTransfer',
                ),
            ],
            database_operations=[],
        ),
    ]
