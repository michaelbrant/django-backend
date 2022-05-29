from rest_framework.renderers import JSONRenderer

'''
ApiRenderer makes all API responses conform to a structure. 
This makes response format predictable.

Success example:
{
  "status": "success",
  "code": 200,
  "data": {"key": "value"},
  "message": None
}

Error example:
{
  "status": "error",
  "code": 400,
  "data": None,
  "message": "Invalid value for field."
}
'''


class ApiRenderer(JSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context['response'].status_code
        response = {
            "status": "success",
            "code": status_code,
            "data": data,
            "message": None
        }

        if not str(status_code).startswith('2'):
            response["status"] = "error"
            response["data"] = None
            try:
                response["message"] = data["detail"]
            except KeyError:
                response["data"] = data
            except AttributeError:
                response["data"] = data
            except TypeError:
                response["data"] = data

        return super(ApiRenderer, self).render(response, accepted_media_type, renderer_context)
