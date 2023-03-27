from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LenderList

router = DefaultRouter()
router.register(r'lenders', LenderList, basename='lenders')

urlpatterns = [
    path('', include(router.urls)),
]
