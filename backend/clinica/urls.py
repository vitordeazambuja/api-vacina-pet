from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PetViewSet, VacinaViewSet, PetVacinaViewSet

router = DefaultRouter()
router.register(r'pets', PetViewSet, basename='pet')
router.register(r'vacinas', VacinaViewSet, basename='vacina')
router.register(r'pet-vacinas', PetVacinaViewSet, basename='petvacina')

urlpatterns = [
    path('', include(router.urls)),
]