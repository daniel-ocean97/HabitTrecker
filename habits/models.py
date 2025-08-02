from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class Habit(models.Model):
    PERIODICITY_CHOICES = [
        (1, 'Ежедневно'),
        (2, 'Каждые 2 дня'),
        (3, 'Каждые 3 дня'),
        (4, 'Каждые 4 дня'),
        (5, 'Каждые 5 дней'),
        (6, 'Каждые 6 дней'),
        (7, 'Раз в неделю'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='habits',
        verbose_name='Пользователь'
    )
    place = models.CharField(
        max_length=255,
        verbose_name='Место выполнения'
    )
    time = models.TimeField(
        verbose_name='Время выполнения'
    )
    action = models.CharField(
        max_length=255,
        verbose_name='Действие'
    )
    is_pleasant = models.BooleanField(
        default=False,
        verbose_name='Признак приятной привычки'
    )
    linked_habit = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='linked_habits',
        verbose_name='Связанная привычка',
        limit_choices_to={'is_pleasant': True}  # Ограничение через админку
    )
    periodicity = models.PositiveSmallIntegerField(
        choices=PERIODICITY_CHOICES,
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(7)],
        verbose_name='Периодичность (дни)'
    )
    reward = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='Вознаграждение'
    )
    duration = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(120)],
        verbose_name='Время на выполнение (секунды)'
    )
    is_public = models.BooleanField(
        default=False,
        verbose_name='Признак публичности'
    )

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
        ordering = ['id']

    def clean(self):
        # Валидация 1: Для приятной привычки запрещены вознаграждения и связи
        if self.is_pleasant:
            if self.reward:
                raise ValidationError(
                    'У приятной привычки не может быть вознаграждения!'
                )
            if self.linked_habit:
                raise ValidationError(
                    'У приятной привычки не может быть связанной привычки!'
                )

        # Валидация 2: Запрет одновременного указания вознаграждения и связанной привычки
        if self.reward and self.linked_habit:
            raise ValidationError(
                'Нельзя указывать одновременно вознаграждение и связанную привычку!'
            )

        # Валидация 3: Связанная привычка должна быть приятной
        if self.linked_habit and not self.linked_habit.is_pleasant:
            raise ValidationError(
                'Связанная привычка должна быть приятной!'
            )

        # Валидация 4: Периодичность не реже 1 раза в 7 дней
        if self.periodicity > 7:
            raise ValidationError(
                'Нельзя выполнять привычку реже, чем 1 раз в 7 дней!'
            )

    def save(self, *args, **kwargs):
        self.full_clean()  # Автоматический вызов валидации при сохранении
        super().save(*args, **kwargs)