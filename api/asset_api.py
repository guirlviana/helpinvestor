from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from core.usecases import asset_usecase
from core.serializers.asset_serializer import AssetSerializer


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_asset(request):
    wallet = request.user.investor.wallet_set.get()
    data = JSONParser().parse(request)
    data['wallet_id'] = wallet.id
    asset = AssetSerializer(data=data)
    
    if not asset.is_valid():
        return JsonResponse(asset.errors, status=400)
    
    try:
        new_asset = asset_usecase.create_asset(
            wallet_id=asset.validated_data['wallet_id'], 
            symbol=asset.validated_data['symbol'],
            buy_price=asset.validated_data['buy_price'],
            sale_price=asset.validated_data['sale_price'],
        )
    except Exception as e:
        return JsonResponse({'response': str(e)}, status=422)

    return JsonResponse({'response': f'Your asset: {new_asset.symbol} has been created'}, status=201)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_assets(request):
    wallet = request.user.investor.wallet_set.get()

    assets = asset_usecase.get_assets(wallet_id=wallet.id)

    return JsonResponse({'response': assets})


@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def edit_asset(request, id):
    wallet = request.user.investor.wallet_set.get()
    data = request.data

    asset = AssetSerializer(data=data, fields_to_validate=data.keys())
    if not asset.is_valid():
        return JsonResponse(asset.errors, status=400)

    try:
        asset_usecase.edit_asset(wallet_id=wallet.id, id=id, new_values=request.data)
    except Exception as e:
        return JsonResponse({'response': str(e)}, status=422)

    return JsonResponse({'response': 'update successfull'})


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def get_share_prices(request):
    alerts = asset_usecase.get_assets_on_target_prices()

    return JsonResponse({'response': alerts}, status=200)