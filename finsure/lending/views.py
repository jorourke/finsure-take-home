from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from rest_framework_json_api import views
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from io import TextIOWrapper
import csv

from rest_framework_json_api.pagination import JsonApiPageNumberPagination

from .models import Lender
from .serializers import LenderSerializer


class ResultPaginator(JsonApiPageNumberPagination):
    page_query_param = "page_number"
    page_size_query_param = "page_length"
    page_size = 5
    max_page_size = 1000


class LenderAPIView(views.ModelViewSet):
    pagination_class = ResultPaginator
    queryset = Lender.objects.all().order_by("created")
    serializer_class = LenderSerializer


@api_view(["POST"])
@parser_classes([MultiPartParser])
def bulk_upload_lenders(request):
    file_obj = request.data["file"]

    if not file_obj.name.endswith(".csv"):
        return Response(
            {"error": "Invalid file type"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        csv_data = TextIOWrapper(file_obj.file, encoding="utf-8")
        reader = csv.DictReader(csv_data)
        lenders = []
        for row in reader:
            serializer = LenderSerializer(data=row)
            if serializer.is_valid():
                lenders.append(serializer.save())
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            LenderSerializer(lenders, many=True).data,
            status=status.HTTP_201_CREATED,
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@require_GET
@csrf_exempt
def lender_csv_download(request):
    lenders = Lender.objects.all()
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="lenders.csv"'
    writer = csv.writer(response)
    # Write CSV header row
    writer.writerow(
        [
            "id",
            "name",
            "code",
            "upfront_commission_rate",
            "trial_commission_rate",
            "active",
        ]
    )
    # Write each Lender as a row in the CSV file
    for lender in lenders:
        writer.writerow(
            [
                lender.id,
                lender.name,
                lender.code,
                lender.upfront_commission_rate,
                lender.trial_commission_rate,
                lender.active,
            ]
        )
    return response
