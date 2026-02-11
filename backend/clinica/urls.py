from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PetViewSet, VacinaViewSet, PetVacinaViewSet

router = DefaultRouter()
router.register(r'pets', PetViewSet)
router.register(r'vacinas', VacinaViewSet)
router.register(r'aplicacoes', PetVacinaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]