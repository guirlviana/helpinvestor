"""
URL configuration for configs project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from api import investor_api, asset_api
from rest_framework.authtoken import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-token-auth/', views.obtain_auth_token),
    path('investor/', investor_api.create_user),
    path('create-asset/', asset_api.create_asset),
    path('get-assets/', asset_api.get_assets),
    path('edit-asset/<int:id>/', asset_api.edit_asset),
    path('delete-asset/<int:id>/', asset_api.delete_asset),
    path('get-share-prices/', asset_api.get_share_prices),
]
