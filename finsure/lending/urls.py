from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LenderAPIView, bulk_upload_lenders, lender_csv_download

# from .views import bulk_upload_lenders

router = DefaultRouter()
router.register(r"lenders", LenderAPIView, basename="lenders")

urlpatterns = [
    path("", include(router.urls)),
    path("lenders_upload/", bulk_upload_lenders, name="bulk_upload_lenders"),
    path("lenders_download/", lender_csv_download, name="lender_csv_download"),
]
