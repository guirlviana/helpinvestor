from django.test import TestCase
from core.usecases.asset_usecase import create_asset
from core.usecases.investor_usecase import create_investor
from db.models import Asset

class CreateAssetTests(TestCase):
    def setUp(self) -> None:
        self.investor = create_investor('john', 'doe', '11999999999', 'email@email.com', 'abcdfg123')
        self.wallet_id = self.investor.wallet_set.get().id
    
    def test_should_create_asset(self):
        data = {
            'wallet_id': self.wallet_id,
            'symbol': 'TAEE4', 
            'buy_price': 10, 
            'sale_price': 15,
        }

        new_asset = create_asset(**data)

        asset = Asset.objects.get(id=new_asset.id)
        self.assertEqual(data['symbol'], asset.symbol)
        self.assertEqual(data['buy_price'], asset.buy_price)
        self.assertEqual(data['sale_price'], asset.sale_price)
