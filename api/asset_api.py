from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
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
    
    new_asset = asset_usecase.create_asset(asset.validated_data['wallet_id'], asset.validated_data['symbol'])

    return JsonResponse({'response': f'Your asset: {new_asset.symbol} has been created'}, status=201)

