from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import HabitViewSet, PublicHabitDetailView, PublicHabitListView

router = DefaultRouter()
router.register(r"habits", HabitViewSet, basename="habits")  # Явный basename

urlpatterns = [
    path("", include(router.urls)),  # Должно быть ПЕРВЫМ элементом
    path("public-habits/", PublicHabitListView.as_view()),
    path("public-habits/<int:pk>/", PublicHabitDetailView.as_view()),
]
