from db.models import Asset

def create_asset(wallet_id, symbol, buy_price, sale_price):
    asset = Asset(symbol=symbol, wallet_id=wallet_id, buy_price=buy_price, sale_price=sale_price)
    asset.save()

    return asset