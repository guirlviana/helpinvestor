from django.test import TestCase
from core.usecases.asset_usecase import create_asset
from core.usecases.investor_usecase import create_investor
from db.models import Asset

class CreateAssetTests(TestCase):
    def setUp(self) -> None:
        self.investor = create_investor('john', 'doe', '11999999999', 'email@email.com', 'abcdfg123')
        self.wallet_id = self.investor.wallet_set.get().id
