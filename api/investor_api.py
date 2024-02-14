from django.http import HttpResponse, JsonResponse
from core.serializers.investor_serializer import InvestorSerializer
from rest_framework.parsers import JSONParser
from core.usecases import investor_usecase
from rest_framework.decorators import api_view


@api_view(['POST'])
def create_user(request):
    data = JSONParser().parse(request)
    investor = InvestorSerializer(data=data)
    
    if not investor.is_valid():
        return JsonResponse(investor.errors, status=400)
    
    validated_data = investor.validated_data
    new_investor = investor_usecase.create_user(
        name=validated_data['name'],
        last_name=validated_data['last_name'],
        phone=validated_data['phone'],
        email=validated_data['email'],
        password=validated_data['password']
    )
    return JsonResponse({'response': f'{new_investor.name}, your investor account has been created'}, status=201)