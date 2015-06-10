# from django.conf.urls import patterns, url, include  # import patterns for format_suffix_patterns
# from rest_framework.urlpatterns import format_suffix_patterns
# from snippets import views
#
# # for tutorial 6: binding ViewSet classes into a set of concrete views
# from snippets.views import SnippetViewSet, UserViewSet, api_root
# from rest_framework import renderers

"""
Added in tutorial 6b: using Routers
"""
from django.conf.urls import url, include
from snippets import views
from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
# Registering the viewsets with the router is similar to providing a urlpattern. We include two arguments -
# the URL prefix for the views, and the viewset itself.
# The DefaultRouter class we're using also automatically creates the API root view for us, so we can now delete
# the api_root method from our views module.
router = DefaultRouter()
router.register(r'snippets', views.SnippetViewSet)
router.register(r'users', views.UserViewSet)

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]



"""
Added in tutorial 6a
Bind ViewSet classes into a set of concrete views
Creating multiple views from each ViewSet class, by binding the http methods to the required action for each view.
"""

# snippet_list = SnippetViewSet.as_view({
#     'get': 'list',
#     'post': 'create'
# })
# snippet_detail = SnippetViewSet.as_view({
#     'get': 'retrieve',
#     'put': 'update',
#     'patch': 'partial_update',
#     'delete': 'destroy'
# })
# snippet_highlight = SnippetViewSet.as_view({
#     'get': 'highlight'
# }, renderer_classes=[renderers.StaticHTMLRenderer])
# user_list = UserViewSet.as_view({
#     'get': 'list'
# })
# user_detail = UserViewSet.as_view({
#   'get': 'retrieve'
# })
#
#
#
# urlpatterns = format_suffix_patterns([
#     url(r'^$', api_root),
#     url(r'^snippets/$', snippet_list, name='snippet-list'),
#     url(r'^snippets/(?P<pk>[0-9]+)/$', snippet_detail, name='snippet-detail'),
#     url(r'^snippets/(?P<pk>[0-9]+)/highlight/$', snippet_highlight, name='snippet-highlight'),
#     url(r'^users/$', user_list, name='user-list'),
#     url(r'^users/(?P<pk>[0-9]+)/$', user_detail, name='user-detail')
# ])

""" Before tutorial 6 """
# # API endpoints
# # urlpatterns = [ ... ]  <-- was this way until tutorial 5, when we changed to hyperlinking:
# # urlpatterns = format_suffix_patterns([ ... ])
# urlpatterns = format_suffix_patterns([
#     # Note: ?P<pk> defines the name that will be used to identify the matched pattern
#     # url(r'^snippets/$', views.snippet_list),                            <-- 1st way
#     # url(r'^snippets/(?P<pk>[0-9]+)/$', views.snippet_detail),
#     url(r'^snippets/$', views.SnippetList.as_view(), name='snippet-list'),
#     url(r'^snippets/(?P<pk>[0-9]+)/$', views.SnippetDetail.as_view(), name='snippet-detail'),  # <-- 2nd way, for using
#                                                                                                # class based views
#     url(r'^users/$', views.UserList.as_view(), name='user-list'),  # added for user views
#     url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view(), name='user-detail'),  # added for user views
#     url(r'^$', views.api_root),  # added for API root [root page/root view/home page(?)] - HTML (not JSON like others!)
#     url(r'^snippets/(?P<pk>[0-9]+)/highlight/$', views.SnippetHighlight.as_view(), name='snippet-highlight'),
#     # Note: added all "name"s in tutorial 5; having a hyperlinked API, we need to name our URL patterns, and these are
#     # the URL patterns that have come up in our code so far:
#     #  - The root of our API refers to 'user-list' and 'snippet-list'.
#     #  - Our snippet serializer includes a field that refers to 'snippet-highlight'.
#     #  - Our user serializer includes a field that refers to 'snippet-detail'.
#     #  - Our snippet and user serializers include 'url' fields that by default will refer to '{model_name}-detail',
#     #    which in this case will be 'snippet-detail' and 'user-detail'.
# ])

"""
Used this until tutorial 5, when it was incorporated above.
"""
# urlpatterns = format_suffix_patterns(urlpatterns)
#     # adds extra url patterns; not necessary but gives us a simple, clean way of referring to a specific format.

"""
Added in tutorial 5; removed in tutorial 6b when using routers
"""
# # Login and logout views for the browsable API
# urlpatterns += [
#     url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
# ]


