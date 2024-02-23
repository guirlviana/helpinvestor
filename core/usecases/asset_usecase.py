from collections import defaultdict
from decimal import Decimal
from db.models import Asset
from services import stock_market_api

def create_asset(wallet_id, symbol, buy_price, sale_price):
    asset = Asset(symbol=symbol, wallet_id=wallet_id, buy_price=buy_price, sale_price=sale_price)
    asset.save()

    return asset

def get_assets_on_target_prices():
    assets = Asset.objects.filter(is_deleted=False).select_related('wallet', 'wallet__investor')
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
        if quote_price:
            for target in targets:
                if Decimal(quote_price) >= target['sale_price']:
                    # opportunity to earn sealling
                    users_to_notify.append({
                        'message': f'{symbol}, reached: R${Decimal(quote_price)} Your alert was set: SALE with {target["sale_price"]} or high',
                        'phone': target['phone'],
                    })
                
                if Decimal(quote_price) <= target['buy_price']:
                    # opportunity to earn buying
                    users_to_notify.append({
                        'message': f'{symbol}, reached: R${Decimal(quote_price)} Your alert was set: BUY with {target["buy_price"]} or lower',
                        'phone': target['phone'],
                    })
    
    return users_to_notify