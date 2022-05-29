from django.contrib import admin
from django.urls import path, re_path
from .app.views import example_views, user_views

API_VERSION = 'api/v1/'


def trigger_error(request):
    division_by_zero = 1 / 0


urlpatterns = [

    path('sentry-debug/', trigger_error),

    path(API_VERSION + 'public', example_views.public),
    path(API_VERSION + 'private', example_views.private),
    path(API_VERSION + 'private-scoped', example_views.private_scoped),

    # Sync User with Auth0
    path(API_VERSION + 'user-sync/',
         user_views.UserDetail.as_view()),
    path(API_VERSION + 'user/',
         user_views.UserDetail.as_view()),

    # Stripe
#     path(API_VERSION + 'create-customer-portal-session/<guild_id>/',
#          stripe_views.get_stripe_session),
#     path(API_VERSION + 'stripe-webhook/',
#          stripe_views.handle_stripe_webhook),

    # Admin Dashboard
    re_path(r'admin\/?', admin.site.urls),

]
