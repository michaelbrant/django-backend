# '''
# This is an example of what a view should look like. Keeping it here for reference.
# '''


# from agrawatt_backend.app.models import Snippet
# from agrawatt_backend.app.serializers import SnippetSerializer
# from agrawatt_backend.app.errors.error_utils import get_validation_error_response, get_general_error_response, get_business_requirement_error_response
# from agrawatt_backend.app.errors.custom_errors import FivetranApiError
# from django.http import Http404
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status


# class SnippetList(APIView):
#     """
#     List all snippets, or create a new snippet.
#     """
#     def get(self, request, format=None):
#         try:
#             snippets = Snippet.objects.all()
#             serializer = SnippetSerializer(snippets, many=True)
#             return Response(serializer.data)
#         except FivetranApiError as e:
#             return get_business_requirement_error_response(e, status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return get_general_error_response(e)

#     def post(self, request, format=None):
#         serializer = SnippetSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return get_validation_error_response(serializer.errors, status.HTTP_400_BAD_REQUEST)

# class SnippetDetail(APIView):
#     """
#     Retrieve, update or delete a snippet instance.
#     """
#     def get_object(self, pk):
#         try:
#             return Snippet.objects.get(pk=pk)
#         except Snippet.DoesNotExist:
#             raise Http404

#     def get(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         serializer = SnippetSerializer(snippet)
#         return Response(serializer.data)

#     def put(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         serializer = SnippetSerializer(snippet, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return get_validation_error_response(serializer.errors, status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
