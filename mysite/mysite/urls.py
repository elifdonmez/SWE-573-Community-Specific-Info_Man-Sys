from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns # new
from django.conf import settings
from django.views.static import serve


from communityinfo.views import register, user_login, home_page, community_creation, \
    community, follow_user, search_communities, edit_rules, share_post, join_community, visit_community, \
    view_profile, edit_profile, post_view, create_post_template, advanced_search

urlpatterns = [
    path('', register, name='register'),  # Root URL mapped to the register view
    path('login', user_login, name='login'),
    path('home', home_page, name='home_page'),
    path('communityCreation', community_creation, name='create_community'),
    path('follow-user/<str:username>/', follow_user, name='follow_user'),
    path('search_communities', search_communities, name='search_communities'),
    path('edit-rules/<str:community_name>/', edit_rules, name='edit_rules'),
    path('share_post/<str:community_name>/', share_post, name='share_post'),
    path('community/<str:community_name>/', community, name='community'),
    path('join-community/<str:community_name>/', join_community, name='join_community'),
    path('visit-community/<str:community_name>/', visit_community, name='visit_community'),
    path('post/<int:post_id>/', post_view, name='post'),
    path('community/<str:community_name>/advanced-search/', advanced_search, name='advanced_search'),
    path('community/<str:community_name>/advanced-search-form/', advanced_search, name='advanced_search_form'),
    path('community/<str:community_name>/advanced-search-results/', advanced_search, name='advanced_search_results'),
    path('profile/', view_profile, name='view_profile'),
    path('edit-profile/', edit_profile, name='edit_profile'),
    path('create_post_template/<str:community_id>/', create_post_template, name='create_post_template'),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),

]

