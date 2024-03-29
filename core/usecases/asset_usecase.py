from collections import defaultdict
from decimal import Decimal
from db.models import Asset
from services import stock_market_api

AVAILABLE_SYMBOLS = ['ITSA4', 'TAEE4', 'BBSE3']

def create_asset(wallet_id, symbol, buy_price, sale_price):
    if symbol not in AVAILABLE_SYMBOLS:
        raise Exception(f'Symbol: {symbol} not valid, options: {", ".join(AVAILABLE_SYMBOLS)}')
    
    asset_already_created = Asset.objects.filter(symbol=symbol, wallet_id=wallet_id).exists()
    if asset_already_created:
        raise Exception(f'Symbol: {symbol} already created')
    
    asset = Asset(symbol=symbol, wallet_id=wallet_id, buy_price=buy_price, sale_price=sale_price)
    asset.save()

    return asset


def get_assets(wallet_id: int):
    fields_available = ('id', 'symbol', 'buy_price', 'sale_price')
    assets = Asset.objects.filter(wallet_id=wallet_id)

    return list(assets.values(*fields_available))


def edit_asset(id: int, wallet_id: int, new_values: dict):
    fields_allowed_update = {'symbol', 'buy_price', 'sale_price'}
    fields_sent = set(new_values.keys())
    if fields_sent - fields_allowed_update:
        raise Exception(f'Fields to update not allowed')
    
    asset = Asset.objects.filter(id=id, wallet_id=wallet_id).exists()
    if not asset:
        raise Exception('Asset does not exists')
    
    Asset.objects.filter(id=id, wallet_id=wallet_id).update(**new_values)


def delete_asset(id: int, wallet_id: int):
    asset = Asset.objects.filter(id=id, wallet_id=wallet_id).exists()
    if not asset:
        raise Exception('Asset does not exists')
    
    Asset.objects.filter(id=id, wallet_id=wallet_id).delete()


def get_assets_on_target_prices():
    assets = Asset.objects.all().select_related('wallet', 'wallet__investor')
    if not assets:
        return
    
    assets_by_symbol = defaultdict(list)
    
    for asset in assets:
        assets_by_symbol[asset.symbol].append(
            {
                'buy_price': asset.buy_price,
                'sale_price': asset.sale_price,
                'phone': asset.wallet.investor.phone
            }
        )
    
    users_to_notify = []
    for symbol, targets in assets_by_symbol.items():
        quote_price = stock_market_api.get_live_quote_price(symbol)
        if not quote_price:
            continue
        
        for target in targets:
            if Decimal(quote_price) >= target['sale_price']:
                # opportunity to earn sealling
                users_to_notify.append({
                    'message': f'{symbol}, reached: R${Decimal(quote_price)} Your alert was set: SALE with R${target["sale_price"]} or high',
                    'phone': target['phone'],
                })
                continue
            
            if Decimal(quote_price) <= target['buy_price']:
                # opportunity to earn buying
                users_to_notify.append({
                    'message': f'{symbol}, reached: R${Decimal(quote_price)} Your alert was set: BUY with R${target["buy_price"]} or lower',
                    'phone': target['phone'],
                })
                continue
    
    return users_to_notify