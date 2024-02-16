from db.models import Assets

def create_asset(wallet_id, symbol):
    asset = Assets(symbol=symbol, wallet_id=wallet_id)
    asset.save()

    return asset