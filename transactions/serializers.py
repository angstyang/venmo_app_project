from rest_framework import serializers
from transactions.models import Transaction


class transactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('id', 'title', 'transaction_url', 'image_path', 'description',
                  'published')
