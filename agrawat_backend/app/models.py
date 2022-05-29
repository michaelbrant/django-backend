import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_api_key.models import AbstractAPIKey
from shortuuid.django_fields import ShortUUIDField


class SubscriptionLimits(models.Model):
    id = models.CharField(primary_key=True, max_length=100, editable=True)
    flow_limit = models.IntegerField()
    can_create_custom_bot = models.BooleanField(default=False)
    can_remove_watermark = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class SubscriptionPlan(models.Model):
    id = models.CharField(primary_key=True, max_length=100, editable=True)
    subscription_limits = models.ForeignKey(
        SubscriptionLimits, on_delete=models.DO_NOTHING, null=True, blank=True)

    def __str__(self):
        return str(self.id)


class SubscriptionPricingPlan(models.Model):
    stripe_price_id = models.CharField(max_length=100)
    subscription_plan = models.ForeignKey(
        SubscriptionPlan, on_delete=models.DO_NOTHING, null=True, blank=True)

    def __str__(self):
        return str(self.stripe_price_id)


class Org(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    site_url = models.URLField(blank=True, null=True)


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    password = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


ROLES = (
    ("ADMIN", "ADMIN"),
    ("USER", "USER"),
)


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    org = models.ForeignKey(
        Org, null=True, on_delete=models.CASCADE, blank=True, related_name="user_org"
    )
    role = models.CharField(max_length=50, choices=ROLES, default="USER")
    #has_sales_access = models.BooleanField(default=False)
    has_billing_access = models.BooleanField(default=False)
    is_organization_admin = models.BooleanField(default=False)

    class Meta:
        unique_together = (("user", "org"),)

    @property
    def is_admin(self):
        return self.is_organization_admin


class OrgAPIKey(AbstractAPIKey):
    org = models.ForeignKey(
        Org,
        on_delete=models.CASCADE,
        related_name="api_keys",
        null=True,
        blank=True
    )


class Auth0Management(models.Model):
    # This table should only have 1 row. It keeps track of the Auth0 M2M token.
    # Auth0 charges a lot of money for M2M tokens, so we just keep the same one for the whole day :)
    id = models.IntegerField(
        primary_key=True, editable=True, unique=True)
    auth0_m2m_token = models.CharField(max_length=5000, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.auth0_m2m_token)
