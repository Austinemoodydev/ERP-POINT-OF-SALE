# Register your models here.
from django.contrib import admin

from .models import (
    User,
    ActivityLog,
    LoginHistory,
    AccountLockout,
    AllowedDevice,
    AllowedIP,


)

admin.site.register(User)
admin.site.register(ActivityLog)
admin.site.register(LoginHistory)
admin.site.register(AccountLockout)
admin.site.register(AllowedDevice)
admin.site.register(AllowedIP)
