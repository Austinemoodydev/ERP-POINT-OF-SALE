from django.contrib import admin
from .models import *

admin.site.register(Company)
admin.site.register(Branch)
admin.site.register(BranchUser)
admin.site.register(BranchTransfer)
admin.site.register(BranchTransferItem)
admin.site.register(BranchRole)
