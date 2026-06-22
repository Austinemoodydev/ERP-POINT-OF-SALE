from django.contrib import admin

# Register your models here.


from .models import *

admin.site.register(Conversation)
admin.site.register(Message)
admin.site.register(Notification)
admin.site.register(WorkTask)
admin.site.register(CalendarEvent)
admin.site.register(Meeting)
admin.site.register(FeatureFlag)
admin.site.register(ErrorLog)
admin.site.register(BackgroundJob)
admin.site.register(Metric)
admin.site.register(ArchivedRecord)
admin.site.register(RetentionPolicy)
