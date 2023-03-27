from rest_framework_json_api import serializers
from .models import Lender


class LenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lender
        fields = [
            "id",
            "name",
            "code",
            "upfront_commission_rate",
            "trial_commission_rate",
            "active",
        ]
