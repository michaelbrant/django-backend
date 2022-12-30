from rest_framework_api_key.permissions import BaseHasAPIKey
from .models import Profile, OrgAPIKey
import logging

logger = logging.getLogger(__file__)


class HasAccountAPIKey(BaseHasAPIKey):
    model = OrgAPIKey


def get_profile_from_auth(request, account_id):
    ''' 
    Users may authenticate with Auth0 or they may use an API Key associated with their account.
    Either way, this function returns the Profile for the authentication used. API key auth return admin user.
    '''
    try:
        auth_type = request.META["HTTP_AUTHORIZATION"].split()[0]
        if auth_type == 'Bearer':
            user = request.user
            profile = Profile.objects.get(user=user, account_id=account_id)
            return profile
        else:
            logger.error(f'Invalid auth type: {auth_type}')
            return False
    except KeyError:
        key = request.headers['X-Api-Key']
        api_key = OrgAPIKey.objects.get_from_key(key)
        return api_key
        # account = api_key.account
        # if not account:
        #     raise Account.DoesNotExist