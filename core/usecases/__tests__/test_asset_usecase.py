from django.test import TestCase
from core.usecases.asset_usecase import create_asset, edit_asset, get_assets
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
        data = {
            'wallet_id': self.wallet_id,
            'symbol': 'TAEE4', 
            'buy_price': 10, 
            'sale_price': 15,
        }
        create_asset(**data)
        data['symbol'] = 'BBSE3'
        create_asset(**data)

        assets = get_assets(self.wallet_id)

        self.assertEqual(2, len(assets))

    
    def test_should_return_only_fields_available(self):
        data = {
            'wallet_id': self.wallet_id,
            'symbol': 'TAEE4', 
            'buy_price': 10, 
            'sale_price': 15,
        }
        create_asset(**data)

        assets = get_assets(self.wallet_id)

        self.assertEqual(1, len(assets))
        asset = assets[0]
        self.assertListEqual(['id', 'symbol', 'buy_price', 'sale_price'], list(asset.keys()))

class EditAsset(AssetsTestCase):
    def test_should_update_only_sent_fields(self):
        asset = self.__create_asset(symbol='BBSE3')

        edit_asset(asset.id, self.wallet_id, new_values={'symbol': 'TAEE4'})

        asset_edited = Asset.objects.get(id=asset.id)
        self.assertEqual('TAEE4', asset_edited.symbol)
        self.assertEqual(asset.buy_price, asset_edited.buy_price)
        self.assertEqual(asset.sale_price, asset_edited.sale_price)
    
    def test_error_when_try_update_not_allowed_fields(self):
        asset = self.__create_asset(symbol='BBSE3')
        
        with self.assertRaises(Exception) as e:
            edit_asset(asset.id, self.wallet_id, new_values={'id': 99})
        
        self.assertEqual('Fields to update not allowed. Allowed fields: buy_price, sale_price, symbol', str(e.exception))
    
    def test_error_when_try_update_assets_that_doesnt_exists(self):
        invalid_id = 1
        with self.assertRaises(Exception) as e:
            edit_asset(invalid_id, self.wallet_id, new_values={})
        
        self.assertEqual('Asset does not exists', str(e.exception))

    def __create_asset(self, **kwargs):
        default = {
            'wallet_id': self.wallet_id,
            'symbol': 'TAEE4', 
            'buy_price': 10, 
            'sale_price': 15,
        } | kwargs

        return create_asset(**default)

class DeleteAsset(AssetsTestCase):
    def test_should_delete_field(self):
        ...
    
    def test_error_when_delete_asset_that_doesnt_exists(self):
        ...
