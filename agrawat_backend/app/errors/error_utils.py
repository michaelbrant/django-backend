from rest_framework.response import Response
from rest_framework import status

# App imports


def get_validation_error_response(validation_error, http_status_code=status.HTTP_400_BAD_REQUEST, display_error=""):
    if display_error == "":
        display_error = "Invalid parameter."
    resp = {
        "error": {
            "display_error": display_error,
            "field_errors": validation_error,
            "internal_error_code": 40000
        }
    }

    return Response(data=resp, status=http_status_code)


def get_general_error_response(display_error="", http_status_code=status.HTTP_400_BAD_REQUEST):
    resp = {
        "error": {
            "display_error": str(display_error),
        }
    }

    return Response(data=resp, status=http_status_code)


def get_business_requirement_error_response(business_logic_error, http_status_code=status.HTTP_400_BAD_REQUEST):
    resp = {
        "error": {
            "display_error": business_logic_error.message,
            "internal_error_code": business_logic_error.internal_error_code,
        }
    }

    return Response(data=resp, status=http_status_code)
