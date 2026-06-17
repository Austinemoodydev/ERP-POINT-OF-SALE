from django.contrib import admin
from .models import (
    CustomerGroup,
    LoyaltyAccount,
    LoyaltyTransaction,
    Reward,
    Promotion,
    Coupon,
    SMSCampaign,
    EmailCampaign,
    WhatsAppMessage,
    CustomerFeedback,
    SupportTicket
)
# Register your models here.
admin.site.register(CustomerGroup)
admin.site.register(LoyaltyAccount)
admin.site.register(LoyaltyTransaction)
admin.site.register(Reward)
admin.site.register(Promotion)
admin.site.register(Coupon)
admin.site.register(SMSCampaign)
admin.site.register(EmailCampaign)
admin.site.register(WhatsAppMessage)
admin.site.register(CustomerFeedback)
admin.site.register(SupportTicket)
