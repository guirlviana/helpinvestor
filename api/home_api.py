from rest_framework.decorators import api_view
from django.http import JsonResponse


@api_view(['GET'])
def welcome(request):
    return JsonResponse(
        {
            'Response': 'Welcome to helpinvetor, check the routes here: https://github.com/guirlviana/helpinvestor#routes'
    }, status=200)
