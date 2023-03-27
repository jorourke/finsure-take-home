from rest_framework_json_api import views
from .models import Lender
from .serializers import LenderSerializer


class LenderList(views.ModelViewSet):
    queryset = Lender.objects.all()
    serializer_class = LenderSerializer
