from decimal import Decimal
from unittest.mock import patch
from django.test import TestCase
from core.usecases.asset_usecase import create_asset, delete_asset, edit_asset, get_assets, get_assets_on_target_prices
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


class EditAssetTests(AssetsTestCase):
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

        self.assertEqual('Fields to update not allowed', str(e.exception))

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


class DeleteAssetTests(AssetsTestCase):
    def test_should_delete_field(self):
        asset = create_asset(
            wallet_id=self.wallet_id,
            symbol='TAEE4',
            buy_price=10,
            sale_price=15,
        )

        delete_asset(asset.id, self.wallet_id)

        self.assertFalse(Asset.objects.filter(id=asset.id).exists())

    def test_error_when_delete_asset_that_doesnt_exists(self):
        invalid_id = 99
        with self.assertRaises(Exception) as e:
            delete_asset(invalid_id, self.wallet_id)

        self.assertEqual('Asset does not exists', str(e.exception))


class GetAssetsOnTargetPricesTests(AssetsTestCase):
    def test_should_return_nothing_when_doesnt_exists_assets(self):
        self.assertIsNone(get_assets_on_target_prices())

    @patch('services.stock_market_api.get_live_quote_price')
    def test_should_return_a_empty_list_when_client_api_doesnt_return_quotes(self, mock_get_live_quote_price):
        mock_get_live_quote_price.return_value = None
        create_asset(
            wallet_id=self.wallet_id,
            symbol='TAEE4',
            buy_price=10,
            sale_price=15,
        )

        self.assertEqual([], get_assets_on_target_prices())

    @patch('services.stock_market_api.get_live_quote_price')
    def test_should_return_asset_when_quote_price_is_greater_or_equal_than_sell_price(self, mock_get_live_quote_price):
        live_quote_price = 10
        sale_price = live_quote_price -1
        mock_get_live_quote_price.side_effect = lambda symbol: live_quote_price if symbol == 'TAEE4' else None
        create_asset(
            wallet_id=self.wallet_id,
            symbol='TAEE4',
            buy_price=2,
            sale_price=sale_price,
        )

        response = get_assets_on_target_prices()

        self.assertEqual(1, len(response))
        asset_to_notify = response[0]
        self.assertEqual(f'TAEE4, reached: R${Decimal(live_quote_price)} Your alert was set: SALE with R${sale_price:.2f} or high', asset_to_notify['message'])
        self.assertEqual(self.investor.phone, asset_to_notify['phone'])

    @patch('services.stock_market_api.get_live_quote_price')
    def test_should_return_asset_when_quote_price_is_less_or_equal_than_buy_price(self, mock_get_live_quote_price):
        live_quote_price = 10
        buy_price = live_quote_price + 1
        mock_get_live_quote_price.side_effect = lambda symbol: live_quote_price if symbol == 'TAEE4' else None
        create_asset(
            wallet_id=self.wallet_id,
            symbol='TAEE4',
            buy_price=buy_price,
            sale_price=50,
        )

        response = get_assets_on_target_prices()

        self.assertEqual(1, len(response))
        asset_to_notify = response[0]
        self.assertEqual(f'TAEE4, reached: R${Decimal(live_quote_price)} Your alert was set: BUY with R${buy_price:.2f} or lower', asset_to_notify['message'])
        self.assertEqual(self.investor.phone, asset_to_notify['phone'])
