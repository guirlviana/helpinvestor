from django.test import TestCase
from core.usecases.asset_usecase import create_asset
from core.usecases.investor_usecase import create_investor
from db.models import Asset

class AssetsTestCase(TestCase):
    def setUp(self) -> None:
        self.investor = create_investor('john', 'doe', '11999999999', 'email@email.com', 'abcdfg123')
        self.wallet_id = self.investor.wallet_set.get().id

class CreateAssetTests(AssetsTestCase):
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
    
    def test_error_when_symbol_not_in_available_symbols(self):
        data = {
            'wallet_id': self.wallet_id,
            'symbol': 'HPIN3', 
            'buy_price': 10, 
            'sale_price': 15,
        }

        with self.assertRaises(Exception) as e:
            create_asset(**data)
        
        self.assertEqual(f"Symbol: {data['symbol']} not valid, options: ITSA4, TAEE4, BBSE3", str(e.exception))


    def test_error_when_try_create_symbol_again(self):
        data = {
            'wallet_id': self.wallet_id,
            'symbol': 'TAEE4', 
            'buy_price': 10, 
            'sale_price': 15,
        }

        create_asset(**data)
        with self.assertRaises(Exception) as e:
            create_asset(**data)
        
        self.assertEqual(f"Symbol: {data['symbol']} already created", str(e.exception))

class GetAssetsTests(AssetsTestCase):
    def test_should_return_all_assets(self):
        ...
    
    def test_should_return_only_fields_available(self):
        ...
