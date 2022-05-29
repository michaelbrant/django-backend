import os
import logging
import stripe

stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')
STRIPE_FREE_PLAN = os.environ.get('STRIPE_FREE_PLAN')


def get_user_stripe_session(stripe_id, return_url):
    try:
        session = stripe.billing_portal.Session.create(
            customer=stripe_id,
            return_url=return_url,
        )
        return session.url
    except Exception as e:
        logging.error(e)


def get_subscription(subscription_id):
    try:
        return stripe.Subscription.retrieve(subscription_id)
    except Exception as e:
        logging.error(e)


def create_stripe_customer(email, name):
    stripe_customer = stripe.Customer.create(
        email=email, name=name)
    return stripe_customer


def set_stripe_customer_on_free_plan(stripe_customer_id):
    stripe.Subscription.create(
        customer=stripe_customer_id,
        items=[
            {"price": STRIPE_FREE_PLAN},
        ]
    )
