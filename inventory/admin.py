from django.contrib import admin

from .models import (
    Warehouse,
    WarehouseStock,
    InventoryLedger,
    StockIn,
    StockInItem,
    StockOut,
    StockOutItem,
    StockAdjustment,
    StockTransfer,
    StockTransferItem,
    DamagedStock,
    ReturnedStock,
    ExpiredStock,
    StockTake,
    StockTakeItem,
    CycleCount,
)

# Register your models here.
admin.site.register(Warehouse)
admin.site.register(WarehouseStock)
admin.site.register(InventoryLedger)
admin.site.register(StockIn)
admin.site.register(StockInItem)
admin.site.register(StockOut)
admin.site.register(StockOutItem)
admin.site.register(StockAdjustment)
admin.site.register(StockTransfer)
admin.site.register(StockTransferItem)
admin.site.register(DamagedStock)
admin.site.register(ReturnedStock)
admin.site.register(ExpiredStock)
admin.site.register(StockTake)
admin.site.register(StockTakeItem)
admin.site.register(CycleCount)
