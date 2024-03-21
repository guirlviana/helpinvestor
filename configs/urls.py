from django.urls import path
from api import investor_api, asset_api, home_api
from rest_framework.authtoken import views

assets_urls = [
    path('create-asset/', asset_api.create_asset),
    path('get-assets/', asset_api.get_assets),
    path('edit-asset/<int:id>/', asset_api.edit_asset),
    path('delete-asset/<int:id>/', asset_api.delete_asset),
]

urlpatterns = [
    path('', home_api.welcome),
    path('api-token-auth/', views.obtain_auth_token),
    path('investor/', investor_api.create_user),
    path('get-share-prices/', asset_api.get_share_prices),
] + assets_urls
