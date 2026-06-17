import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_branchtransfer_branchtransferitem'),
        ('products', '0002_product_productimage_productlocation_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productserial',
            name='action',
        ),
        migrations.RemoveField(
            model_name='productserial',
            name='quantity',
        ),
        migrations.AddField(
            model_name='inventoryaudit',
            name='action',
            field=models.CharField(
                default='',
                max_length=255
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='inventoryaudit',
            name='created_at',
            field=models.DateTimeField(
                auto_now_add=True,
                default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='inventoryaudit',
            name='product',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to='products.product'
            ),
        ),
        migrations.AddField(
            model_name='inventoryaudit',
            name='quantity',
            field=models.DecimalField(
                decimal_places=2,
                default=0,
                max_digits=15
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='inventoryaudit',
            name='product',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to='products.product'
            ),
        ),
    ]
