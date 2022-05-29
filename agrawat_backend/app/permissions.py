from rest_framework_api_key.permissions import BaseHasAPIKey
from .models import Org, Profile, User, OrgAPIKey
import logging

logger = logging.getLogger(__file__)


class HasOrgAPIKey(BaseHasAPIKey):
    model = OrgAPIKey


def get_permissions_from_auth(request):
    ''' 
    Users may authenticate with Auth0 or they may use an API Key associated with their org.
    Either way, this function returns the Profile for the authentication used. API key auth return admin user.
    '''
    try:
        auth_type = request.META["HTTP_AUTHORIZATION"].split()[0]
        if auth_type == 'Bearer':
            user = request.user
            profile = Profile.objects.get(user=user)
            return profile
        else:
            logger.error(f'Invalid auth type: {auth_type}')
            return False
    except Exception:
        key = request.headers['X-Api-Key']
        api_key = OrgAPIKey.objects.get_from_key(key)
        return api_key
        # org = api_key.org
        # if not org:
        #     raise Org.DoesNotExist
        # profile = Profile.objects.get(org=org, is_organization_admin=True)
        # return profile
