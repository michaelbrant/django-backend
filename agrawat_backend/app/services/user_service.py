import os
import requests
from agrawat_backend.app.serializers import UserPublicSerializer
from agrawat_backend.app.models import Auth0Management
# from agrawat_backend.app.errors.custom_errors import EmailError
from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Personalization, Email
import logging
import urllib.parse
from datetime import datetime, timezone

logger = logging.getLogger(__file__)


def generate_auth0_key():
    url = f'https://{settings.AUTH0_DOMAIN}/oauth/token'
    m2m_client_id = os.environ.get('AUTH0_M2M_CLIENT_ID')
    m2m_client_secret = os.environ.get('AUTH0_M2M_CLIENT_SECRET')
    m2m_audience = urllib.parse.quote(os.environ.get('AUTH0_M2M_AUDIENCE'))
    payload = f'grant_type=client_credentials&client_id={m2m_client_id}&client_secret={m2m_client_secret}&audience={m2m_audience}'
    headers = {
        'content-type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()['access_token']


def refresh_auth0_management_key():
    new_token = generate_auth0_key()
    try:
        auth0_m2m_object = Auth0Management.objects.get(id=0)
    except Exception:
        auth0_m2m_object = Auth0Management.objects.create(id=0)
    auth0_m2m_object.auth0_m2m_token = new_token
    auth0_m2m_object.save()
    return new_token


def get_auth0_management_key():
    try:
        auth0_m2m_object = Auth0Management.objects.get(id=0)
    except Exception:
        auth0_m2m_object = Auth0Management.objects.create(id=0)
    now = datetime.now(timezone.utc)
    difference = now - auth0_m2m_object.updated_at
    if difference.seconds < 82800:  # 23 hours
        return auth0_m2m_object.auth0_m2m_token
    else:
        return refresh_auth0_management_key()


def get_user_details(auth0_access_token, username):
    my_headers = {'Authorization': f'Bearer {auth0_access_token}'}
    response = requests.get(
        f'https://{settings.AUTH0_DOMAIN}/api/v2/users/{username}', headers=my_headers)
    if response.status_code != 200:
        raise
    return response.json()


def get_first_name(fullname):
    firstname = ''
    try:
        firstname = fullname.split()[0]
    except Exception as e:
        logging.warning(e)
    return firstname


def get_last_name(fullname):
    lastname = ''
    try:
        index = 0
        for part in fullname.split():
            if index > 0:
                if index > 1:
                    lastname += ' '
                lastname += part
            index += 1
    except Exception as e:
        logging.warning(e)
    return lastname


def sync_user(user):
    auth0_access_token = get_auth0_management_key()
    try:
        user_details = get_user_details(
            auth0_access_token, user.username.replace('.', '|'))
    except Exception:
        auth0_access_token = refresh_auth0_management_key()
        user_details = get_user_details(
            auth0_access_token, user.username.replace('.', '|'))
    access_token = user_details['identities'][0]['access_token']
    refresh_token = user_details['identities'][0]['refresh_token']
    name = user_details.get('name', '')
    email = user_details.get('email', '')

    user.first_name = get_first_name(name)
    user.last_name = get_last_name(name)
    user.email = email
    user.access_token = access_token
    user.refresh_token = refresh_token
    user.save()

    serializer = UserPublicSerializer(user)
    return serializer.data


# def email_user(to_email, template_id, substitutions={}):
#     message = Mail(
#         from_email=('support@voicepopcorn.com', 'VoicePopcorn'))
#     p = Personalization()
#     p.add_to(Email(to_email))
#     p.dynamic_template_data = substitutions
#     message.add_personalization(p)
#     message.template_id = template_id

#     try:
#         sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
#         sg.send(message)
#     except Exception as e:
#         logging.error(e)
#         raise EmailError(e)
