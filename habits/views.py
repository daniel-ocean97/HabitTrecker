from rest_framework import generics, permissions, viewsets

from habits.models import Habit
from habits.paginators import MyPagination
from habits.serializers import HabitSerializer


class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    pagination_class = MyPagination

    def get_queryset(self):
        from .models import Habit  # Локальный импорт!

        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PublicHabitListView(generics.ListAPIView):
    """
    Эндпоинт для просмотра публичных привычек (только список)
    """

    queryset = Habit.objects.filter(is_public=True)
    serializer_class = HabitSerializer
    permission_classes = [permissions.AllowAny]  # Доступ без авторизации
    pagination_class = MyPagination


class PublicHabitDetailView(generics.RetrieveAPIView):
    """
    Эндпоинт для детального просмотра публичной привычки
    """

    queryset = Habit.objects.filter(is_public=True)
    serializer_class = HabitSerializer
    permission_classes = [permissions.AllowAny]  # Доступ без авторизации
    lookup_field = "pk"
