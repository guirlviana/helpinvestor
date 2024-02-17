from rest_framework import serializers

class AssetSerializer(serializers.Serializer):
    symbol = serializers.CharField(max_length=8, required=True)
    wallet_id = serializers.IntegerField(min_value=1, required=True)
    buy_price = serializers.DecimalField(min_value=1, decimal_places=2, max_digits=5)
    sale_price = serializers.DecimalField(min_value=1, decimal_places=2, max_digits=5)