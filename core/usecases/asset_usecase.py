from db.models import Assets

def create_asset(wallet_id, symbol, buy_price, sale_price):
    asset = Assets(symbol=symbol, wallet_id=wallet_id, buy_price=buy_price, sale_price=sale_price)
    asset.save()

    return asset