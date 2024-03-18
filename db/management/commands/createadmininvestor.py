from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.serializers.investor_serializer import InvestorSerializer

from core.usecases.investor_usecase import create_investor


class Command(BaseCommand):
    help = 'Create an admin investor, admin investor can get live quote prices'
