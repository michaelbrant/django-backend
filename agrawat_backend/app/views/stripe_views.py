import logging
import os
from agrawat_backend.app.services.stripe_service import get_user_stripe_session, set_stripe_customer_on_free_plan
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.http import Http404, HttpResponse, JsonResponse
from agrawat_backend.app.models import DiscoGuild, SubscriptionPlan, SubscriptionPricingPlan
import stripe


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_stripe_session(request, guild_id):
    # TODO check that user is the billing manager of this guild
    disco_guild = DiscoGuild.objects.get(id=guild_id)
    DEFAULT_REDIRECT_URL = os.environ.get('STRIPE_REDIRECT_URL')

    return_url = request.GET.get('returnUrl', DEFAULT_REDIRECT_URL)
    stripe_url = get_user_stripe_session(disco_guild.stripe_id, return_url)
    return JsonResponse({'stripe_url': stripe_url})


@api_view(['POST'])
@permission_classes([AllowAny])
def handle_stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    endpoint_secret = os.environ.get('STRIPE_ENDPOINT_SECRET')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the event
    if event['type'] == 'customer.subscription.deleted':
        # Always put on free plan when anything is canceled
        try:
            customer_id = event['data']['object']['customer']
            pricing_plan = event['data']['object']['plan']['id']
            free_subscription_plan = SubscriptionPlan.objects.get(
                id='FREE_PLAN')
            disco_guild = DiscoGuild.objects.get(stripe_id=customer_id)
            logging.info(
                f'Moving Disco Guild {disco_guild.id} to the FREE plan.')
            disco_guild.subscription_plan = free_subscription_plan
            disco_guild.save()
            set_stripe_customer_on_free_plan(customer_id)
        except SubscriptionPlan.DoesNotExist:
            logging.error(f'FREE Subscription plan not found!')
            raise Http404
        except DiscoGuild.DoesNotExist:
            logging.error(
                f'Disco guild with stripe ID {customer_id} not found! Cant put on free plan.')
            raise Http404
    elif event['type'] == 'customer.subscription.created' or event['type'] == 'customer.subscription.updated':
        try:
            # Get the pricing plan id and set the plan in DB
            pricing_plan = event['data']['object']['plan']['id']
            customer_id = event['data']['object']['customer']
            disco_guild = DiscoGuild.objects.get(stripe_id=customer_id)
            subscription_pricing_plan = SubscriptionPricingPlan.objects.get(
                stripe_price_id=pricing_plan)
            disco_guild.subscription_plan = subscription_pricing_plan.subscription_plan
            disco_guild.save()
        except DiscoGuild.DoesNotExist:
            logging.error(
                f'Disco guild with stripe ID {customer_id} not found! Cant put on free plan.')
            raise Http404
        except SubscriptionPricingPlan.DoesNotExist:
            logging.error(f'Subscription pricing plan not found!')
            raise Http404
    else:
        print('Unhandled stripe event type {}'.format(event['type']))

    return JsonResponse({'message': 'handled'})
