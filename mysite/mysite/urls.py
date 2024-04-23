"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from communityinfo.views import register, user_login, home_page, community_creation, \
    community, follow_user, search_communities, edit_rules, share_post, join_community, visit_community, \
    view_profile, edit_profile, post_view

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
    path('join-community/<str:community_name>/', join_community, name='community'),
    path('visit-community/<str:community_name>/', visit_community, name='visit_community'),
    path('post/<int:post_id>/', post_view, name='post'),
    path('profile/', view_profile, name='view_profile'),
    path('edit-profile/', edit_profile, name='edit_profile'),
    # Update the URL pattern for the community view
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)