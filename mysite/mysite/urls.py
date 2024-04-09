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
from django.urls import path
from communityinfo.views import register, user_login, home_page, community_creation, join_community  # Import your registration view

urlpatterns = [
    path('', register, name='register'),  # Root URL mapped to the register view
    path('login', user_login, name='login'),
    path('home', home_page, name='home_page'),
    path('communityCreation', community_creation, name='create_community'),
    path('join-community/<str:community_name>/', join_community, name='join_community'),

]