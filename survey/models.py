import pytz
from django import template
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone

from quizes.settings import TIME_ZONE

register = template.Library()


class Question(models.Model):
    created = models.DateField("Creada", auto_now_add=True)
    author = models.ForeignKey(
        get_user_model(),
        related_name="questions",
        verbose_name="Pregunta",
        on_delete=models.CASCADE,
    )
    title = models.CharField("Título", max_length=200)
    description = models.TextField("Descripción")

    def user_value(self, user):
        try:
            return self.answers.get(author=user).value
        except Answer.DoesNotExist:
            return 0

    def user_likes(self, user):
        return self.likes_dislikes.filter(author=user, value=1).exists()

    def user_dislikes(self, user):
        return self.likes_dislikes.filter(author=user, value=-1).exists()

    def ranking(self):
        """
        - Cada respuesta suma 10 puntos al ranking
        - Cada like suma 5 puntos al ranking
        - Cada dislike resta 3 puntos al ranking
        - Las preguntas del día de hoy, tienen un extra de 10 puntos
        """
        today = timezone.now().astimezone(pytz.timezone(TIME_ZONE)).date()
        created = self.created
        days = (today - created).days
        print(days)
        return (
            self.answers.count() * 10
            + self.likes_dislikes.filter(value=1).count() * 5
            - self.likes_dislikes.filter(value=-1).count() * 3
            + (10 if days == 0 else 0)
        )

    def get_absolute_url(self):
        return reverse("survey:question-edit", args=[self.pk])


class Answer(models.Model):
    ANSWERS_VALUES = (
        (0, "Sin Responder"),
        (1, "Muy Bajo"),
        (2, "Bajo"),
        (3, "Regular"),
        (4, "Alto"),
        (5, "Muy Alto"),
    )

    question = models.ForeignKey(
        Question,
        related_name="answers",
        verbose_name="Pregunta",
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        get_user_model(),
        related_name="answers",
        verbose_name="Autor",
        on_delete=models.CASCADE,
    )
    value = models.PositiveIntegerField("Respuesta", default=0)
    comment = models.TextField("Comentario", default="", blank=True)


class LikeDislike(models.Model):
    author = models.ForeignKey(
        get_user_model(),
        related_name="likes_dislikes",
        verbose_name="LikeDislike",
        on_delete=models.CASCADE,
    )
    question = models.ForeignKey(
        Question,
        related_name="likes_dislikes",
        verbose_name="LikeDislike",
        on_delete=models.CASCADE,
    )
    LIKE_DISLIKE_VALUES = ((1, "Like"), (-1, "Dislike"))
    value = models.SmallIntegerField(
        "Like/Dislike", choices=LIKE_DISLIKE_VALUES, default=1
    )

    class Meta:
        # an user can only give one like or dislike to a question
        unique_together = ("author", "question")
