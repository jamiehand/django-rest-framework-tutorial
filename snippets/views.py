from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer

# tutorial 4:
from django.contrib.auth.models import User  # for creating user views
from snippets.serializers import UserSerializer  # for creating user views
from rest_framework import permissions  # for making sure only authenticated users have more than read-only access
from snippets.permissions import IsOwnerOrReadOnly  # for custom permission in permissions.py

# tutorial 5:
from rest_framework.decorators import api_view  # these 3: for using a regular function-based view & @api_view decorator
from rest_framework.response import Response    # to create a single entry point to our API
from rest_framework.reverse import reverse
from rest_framework import renderers          # these 2: for presenting an HTML representation as opposed to using JSON:
from rest_framework.response import Response  # creating our own .get() method

# tutorial 6:
from rest_framework import viewsets
from rest_framework.decorators import detail_route

"""
From tutorial 1
"""
# class JSONResponse(HttpResponse):
#     """
#     An HttpResponse that renders its content into JSON.
#     """
#     def __init__(self, data, **kwargs):
#         content = JSONRenderer().render(data)
#         kwargs['content_type'] = 'application/json'
#         super(JSONResponse, self).__init__(content, **kwargs)
#
#     ** Should the following 2 def's be inside "JSONResponse(HttpResponse)"? Tutorial wasn't very clear, but I think
#     ** they should be.
#
#     # The root of our API: a view that supports listing all the existing snippets, or creating a new snippet.
#     @csrf_exempt  # because we want to be able to POST to this view from clients that won't have a CSRF token.
#     def snippet_list(request):
#         """
#         List all code snippets, or create a new snippet.
#         """
#         if request.method == 'GET':
#             snippets = Snippet.objects.all()
#             serializer = SnippetSerializer(snippets, many=True)
#             return JSONResponse(serializer.data)
#
#         elif request.method == 'POST':
#             data = JSONParser().parse(request)
#             serializer = SnippetSerializer(data=data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return JSONResponse(serializer.data, status=201)
#             return JSONResponse(serializer.errors, status=400)
#
#     # A view which corresponds to an individual snippet, and can be used to retrieve, update or delete the snippet.
#     @csrf_exempt
#     def snippet_detail(request, pk):
#         """
#         Retrieve, update or delete a code snippet.
#         """
#         try:
#             snippet = Snippet.objects.get(pk=pk)
#         except Snippet.DoesNotExist:
#             return HttpResponse(status=404)
#
#         if request.method == 'GET':
#             serializer = SnippetSerializer(snippet)
#             return JSONResponse(serializer.data)
#
#         elif request.method == 'PUT':
#             data = JSONParser().parse(request)
#             serializer = SnippetSerializer(snippet, data=data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return JSONResponse(serializer.data)
#             return JSONResponse(serializer.errors, status=400)
#
#         elif request.method == 'DELETE':
#             snippet.delete()
#             return HttpResponse(status=204)

"""
Added in tutorial 2
Note: we're no longer explicitly tying our requests or responses to a given content type [like json]. request.data can
handle incoming json requests, but it can also handle other formats. Similarly we're returning response objects with
data, but allowing REST framework to render the response into the correct content type for us.
"""
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


# @api_view(['GET', 'POST'])
# def snippet_list(request, format=None):
#         # Adding "format" lets us explicitly refer to a specific format and means API will be able to handle URLs like:
#         # http://example.com/api/items/4/.json
#         # In conjunction with this, add a set of format_suffix_patterns in snippets/urls.py.
#     """
#     List all snippets, or create a new snippet.
#     """
#     if request.method == 'GET':
#         snippets = Snippet.objects.all()
#         serializer = SnippetSerializer(snippets, many=True)
#         return Response(serializer.data)
#
#     elif request.method == 'POST':
#         serializer = SnippetSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def snippet_detail(request, pk, format=None):
#     """
#     Retrieve, update or delete a snippet instance.
#     """
#     try:
#         snippet = Snippet.objects.get(pk=pk)
#     except Snippet.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'GET':
#         serializer = SnippetSerializer(snippet)
#         return Response(serializer.data)
#
#     elif request.method == 'PUT':
#         serializer = SnippetSerializer(snippet, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     elif request.method == 'DELETE':
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


"""
Added in tutorial 3a
Change to using class based views --> need to refactor snippets/urls.py, as well.
"""
from django.http import Http404
from rest_framework.views import APIView

# class SnippetList(APIView):
#     """
#     List all snippets, or create a new snippet.
#     """
#     def get(self, request, format=None):
#         snippets = Snippet.objects.all()
#         serializer = SnippetSerializer(snippets, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = SnippetSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# class SnippetDetail(APIView):
#     """
#     Retrieve, update or delete a snippet instance.
#     """
#     def get_object(self, pk):
#         try:
#             return Snippet.objects.get(pk=pk)
#         except Snippet.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         serializer = SnippetSerializer(snippet)
#         return Response(serializer.data)
#
#     def put(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         serializer = SnippetSerializer(snippet, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

"""
Added in tutorial 3b
Change to using REST framework's "mixin" classes
"""
from rest_framework import mixins
from rest_framework import generics

# # Building the view using GenericAPIView (class base - provides core functionality), and adding in ListModelMixin and
# # CreateModelMixin (mixin classes - provide .list() and .create() actions). Then, explicitly binding "get" and "post"
# # methods to the appropriate actions.
# class SnippetList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
#
# #  Using the GenericAPIView class to provide the core functionality, and adding in mixins to provide the .retrieve(),
# # .update() and .destroy() actions.
# class SnippetDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,
#                     generics.GenericAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
#
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)

"""
Added in tutorial 3c
Change to using already mixed-in generic views
(Only the following imports are needed, and they're imported above:
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework import generics)
"""

# class SnippetList(generics.ListCreateAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
#
#     # Causes the create() method of our serializer to be passed an additional 'owner' field, along with the
#     # validated data from the request. (Associates snippets w/ the user that created them.)
#     # ** After creating this, update SnippetSerializer to refelct it.
#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)
#
# class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

# Tutorial 6: replace the above 2 classes, plus SnippetHighlight, with a single UserViewSet (see below).

"""
Added in tutorial 4
Creating read-only views for user representations
** Then add these views into the API by referencing them from the URL conf. -- Add to patterns in urls.py.
"""

# class UserList(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
# class UserDetail(generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

# Tutorial 6: replace the above 2 classes with a single UserViewSet:
class UserViewSet(viewsets.ReadOnlyModelViewSet):  # provides default 'read-only' operations
    """
    This viewset automatically provides 'list' and 'detail' actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

"""
Added in tutorial 5
Use a regular function-based view & @api_view decorator to create a single entry point to our API
Note: 1. we're using REST framework's reverse function in order to return fully-qualified URLs;
2. URL patterns are identified by convenience names that we will declare later on in our snippets/urls.py.
** Then (as usual!) add the new views in to the URLconf. -- add a url pattern for the new API root in snippets/urls.py.
"""

@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })

# class SnippetHighlight(generics.GenericAPIView):
#     queryset = Snippet.objects.all()
#     renderer_classes = (renderers.StaticHTMLRenderer,)
#
#     def get(self, request, *args, **kwargs):
#         snippet = self.get_object()
#         return Response(snippet.highlighted)

# Tutorial 6: replace SnippetList, SnippetDetail, and SnippetHighlight view classes w/ a single UserViewSet:
class SnippetViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides 'list', 'create', 'retrieve', 'update', and 'destroy' actions.
    Additionally we also provide an extra 'highlight' action.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    # Using the @detail_route decorator to create a custom action, named highlight. This decorator can be used to
    # add any custom endpoints that don't fit into the standard create/update/delete style.
    # Custom actions which use the @detail_route decorator will respond to GET requests. We can use the methods
    # argument if we wanted an action that responded to POST requests.
    # The URLs for custom actions by default depend on the method name itself. If you want to change the way url
    # should be constructed, you can include url_path as a decorator keyword argument.
    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)



