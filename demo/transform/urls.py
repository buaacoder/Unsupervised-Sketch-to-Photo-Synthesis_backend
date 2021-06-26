from django.urls import path, include
from rest_framework.routers import DefaultRouter
from transform import views

router = DefaultRouter()
router.register('transform', views.Transform)

urlpatterns = [
    path('', include(router.urls)),
]
