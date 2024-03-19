from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.serializers.investor_serializer import InvestorSerializer

from core.usecases.investor_usecase import create_investor


class Command(BaseCommand):
    help = 'Create an admin investor, admin investor can get live quote prices'

    def add_arguments(self, parser):
        parser.add_argument('name', type=str, help='Investor name')
        parser.add_argument('last_name', type=str, help='Investor last_name')
        parser.add_argument('email', type=str, help='Investor email')
        parser.add_argument('password', type=str, help='Investor password')
        parser.add_argument('phone', type=str, help='Investor phone')

    def handle(self, *args, **options):
        investor = InvestorSerializer(data=options)
    
        if not investor.is_valid():
            self.stdout.write(self.style.ERROR('Invalid params'))
        
        validated_data = investor.validated_data
        try:
            new_investor = create_investor(
                name=validated_data['name'],
                last_name=validated_data['last_name'],
                phone=validated_data['phone'],
                email=validated_data['email'],
                password=validated_data['password']
            )
            User.objects.filter(id=new_investor.user_id).update(is_staff=True)
        except Exception as e:
            self.stdout.write(self.style.ERROR(str(e)))
        else:
            self.stdout.write(self.style.SUCCESS('Successfully created admin investor!'))
