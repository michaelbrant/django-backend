from django.contrib import admin
from .models import Org, OrgAPIKey, User, Org, Profile, SubscriptionLimits, SubscriptionPlan, SubscriptionPricingPlan
from rest_framework_api_key.admin import APIKeyModelAdmin, APIKey


# Register your models here.
admin.site.register(User)
admin.site.register(Org)
admin.site.register(Profile)
admin.site.register(SubscriptionLimits)
admin.site.register(SubscriptionPlan)
admin.site.register(SubscriptionPricingPlan)


@admin.register(OrgAPIKey)
class OrgAPIKeyModelAdmin(APIKeyModelAdmin):
    pass


# Don't show the parent APIKey model on admin page, only our custom one
admin.site.unregister(APIKey)
