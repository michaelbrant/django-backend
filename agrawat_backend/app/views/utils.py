from django.http.response import JsonResponse
import jwt
from functools import wraps


def filter_allowed_fields(allowed_fields, data):
    result_data = {}
    for allowed_field in allowed_fields:
        value = data.get(allowed_field, None)
        if value != None:
            result_data[allowed_field] = value
    return result_data


def remove_disallowed_fields(disallowed_fields, data):
    for disallowed_field in disallowed_fields:
        try:
            data.pop(disallowed_field)
        except Exception as e:
            pass
    return data


def get_token_auth_header(request):
    """Obtains the access token from the Authorization Header
    """
    auth = request.META.get("HTTP_AUTHORIZATION", None)
    parts = auth.split()
    token = parts[1]

    return token


def requires_scope(required_scope):
    """Determines if the required scope is present in the access token
    Args:
        required_scope (str): The scope required to access the resource
    """
    def require_scope(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = get_token_auth_header(args[0])
            decoded = jwt.decode(token, verify=False)
            if decoded.get("scope"):
                token_scopes = decoded["scope"].split()
                for token_scope in token_scopes:
                    if token_scope == required_scope:
                        return f(*args, **kwargs)
            response = JsonResponse(
                {'message': 'You don\'t have access to this resource'})
            response.status_code = 403
            return response
        return decorated
    return require_scope
